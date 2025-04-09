#!/usr/bin/env python3
import os
import sys
import psycopg2
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseIntegrityChecker:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME', 'misacash')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_password = os.getenv('DB_PASSWORD', '')
        
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            return psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                host=self.db_host,
                password=self.db_password
            )
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco: {str(e)}")
            return None
    
    def check_table_integrity(self, conn) -> List[Dict[str, Any]]:
        """Verifica a integridade das tabelas"""
        issues = []
        try:
            with conn.cursor() as cur:
                # Listar todas as tabelas
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = cur.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    
                    # Verificar registros órfãos
                    cur.execute(f"""
                        SELECT COUNT(*) 
                        FROM {table_name} t
                        LEFT JOIN users u ON t.user_id = u.id
                        WHERE t.user_id IS NOT NULL AND u.id IS NULL
                    """)
                    orphaned = cur.fetchone()[0]
                    if orphaned > 0:
                        issues.append({
                            'table': table_name,
                            'type': 'orphaned_records',
                            'count': orphaned
                        })
                    
                    # Verificar registros duplicados
                    cur.execute(f"""
                        SELECT COUNT(*) 
                        FROM (
                            SELECT id, COUNT(*) 
                            FROM {table_name} 
                            GROUP BY id 
                            HAVING COUNT(*) > 1
                        ) duplicates
                    """)
                    duplicates = cur.fetchone()[0]
                    if duplicates > 0:
                        issues.append({
                            'table': table_name,
                            'type': 'duplicate_records',
                            'count': duplicates
                        })
                    
                    # Verificar registros inconsistentes
                    cur.execute(f"""
                        SELECT COUNT(*) 
                        FROM {table_name} 
                        WHERE created_at > updated_at
                    """)
                    inconsistent = cur.fetchone()[0]
                    if inconsistent > 0:
                        issues.append({
                            'table': table_name,
                            'type': 'inconsistent_dates',
                            'count': inconsistent
                        })
        
        except Exception as e:
            logger.error(f"Erro ao verificar integridade das tabelas: {str(e)}")
        
        return issues
    
    def check_index_integrity(self, conn) -> List[Dict[str, Any]]:
        """Verifica a integridade dos índices"""
        issues = []
        try:
            with conn.cursor() as cur:
                # Verificar índices não utilizados
                cur.execute("""
                    SELECT schemaname, tablename, indexname
                    FROM pg_stat_user_indexes
                    WHERE idx_scan = 0
                """)
                unused_indexes = cur.fetchall()
                for idx in unused_indexes:
                    issues.append({
                        'schema': idx[0],
                        'table': idx[1],
                        'index': idx[2],
                        'type': 'unused_index'
                    })
                
                # Verificar índices fragmentados
                cur.execute("""
                    SELECT schemaname, tablename, indexname, 
                           CASE WHEN avg_leaf_density < 0.5 THEN 'high' 
                                WHEN avg_leaf_density < 0.8 THEN 'medium' 
                                ELSE 'low' END as fragmentation
                    FROM pg_stat_user_indexes
                    WHERE avg_leaf_density < 0.8
                """)
                fragmented_indexes = cur.fetchall()
                for idx in fragmented_indexes:
                    issues.append({
                        'schema': idx[0],
                        'table': idx[1],
                        'index': idx[2],
                        'type': 'fragmented_index',
                        'fragmentation': idx[3]
                    })
        
        except Exception as e:
            logger.error(f"Erro ao verificar integridade dos índices: {str(e)}")
        
        return issues
    
    def check_constraint_integrity(self, conn) -> List[Dict[str, Any]]:
        """Verifica a integridade das constraints"""
        issues = []
        try:
            with conn.cursor() as cur:
                # Verificar violações de chaves estrangeiras
                cur.execute("""
                    SELECT tc.table_name, tc.constraint_name
                    FROM information_schema.table_constraints tc
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                """)
                foreign_keys = cur.fetchall()
                
                for fk in foreign_keys:
                    table_name = fk[0]
                    constraint_name = fk[1]
                    
                    cur.execute(f"""
                        SELECT COUNT(*) 
                        FROM {table_name} t
                        WHERE NOT EXISTS (
                            SELECT 1 
                            FROM referenced_table r 
                            WHERE t.referenced_column = r.id
                        )
                    """)
                    violations = cur.fetchone()[0]
                    if violations > 0:
                        issues.append({
                            'table': table_name,
                            'constraint': constraint_name,
                            'type': 'foreign_key_violation',
                            'count': violations
                        })
        
        except Exception as e:
            logger.error(f"Erro ao verificar integridade das constraints: {str(e)}")
        
        return issues
    
    def check_data_consistency(self, conn) -> List[Dict[str, Any]]:
        """Verifica a consistência dos dados"""
        issues = []
        try:
            with conn.cursor() as cur:
                # Verificar saldos inconsistentes
                cur.execute("""
                    SELECT user_id, 
                           SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) as balance,
                           expected_balance
                    FROM transactions t
                    JOIN user_balances ub ON t.user_id = ub.user_id
                    GROUP BY t.user_id, ub.expected_balance
                    HAVING SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) != expected_balance
                """)
                inconsistent_balances = cur.fetchall()
                for balance in inconsistent_balances:
                    issues.append({
                        'user_id': balance[0],
                        'type': 'inconsistent_balance',
                        'actual': balance[1],
                        'expected': balance[2]
                    })
                
                # Verificar datas inconsistentes
                cur.execute("""
                    SELECT id, created_at, updated_at
                    FROM transactions
                    WHERE created_at > updated_at
                """)
                inconsistent_dates = cur.fetchall()
                for date in inconsistent_dates:
                    issues.append({
                        'id': date[0],
                        'type': 'inconsistent_dates',
                        'created_at': date[1],
                        'updated_at': date[2]
                    })
        
        except Exception as e:
            logger.error(f"Erro ao verificar consistência dos dados: {str(e)}")
        
        return issues
    
    def run(self):
        """Executa todas as verificações de integridade"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            all_issues = []
            
            # Verificar tabelas
            table_issues = self.check_table_integrity(conn)
            all_issues.extend(table_issues)
            
            # Verificar índices
            index_issues = self.check_index_integrity(conn)
            all_issues.extend(index_issues)
            
            # Verificar constraints
            constraint_issues = self.check_constraint_integrity(conn)
            all_issues.extend(constraint_issues)
            
            # Verificar consistência dos dados
            data_issues = self.check_data_consistency(conn)
            all_issues.extend(data_issues)
            
            # Reportar resultados
            if all_issues:
                logger.warning(f"Encontrados {len(all_issues)} problemas de integridade")
                for issue in all_issues:
                    logger.warning(f"Problema: {issue}")
            else:
                logger.info("Nenhum problema de integridade encontrado")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro durante a verificação de integridade: {str(e)}")
            return False
            
        finally:
            conn.close()

if __name__ == '__main__':
    checker = DatabaseIntegrityChecker()
    success = checker.run()
    sys.exit(0 if success else 1) 