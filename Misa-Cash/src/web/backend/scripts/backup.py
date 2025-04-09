#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
import boto3
from botocore.exceptions import ClientError
import logging
from typing import Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME', 'misacash')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.backup_dir = os.getenv('BACKUP_DIR', '/var/backups/misacash')
        self.retention_days = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
        self.s3_bucket = os.getenv('BACKUP_S3_BUCKET', '')
        self.compress = os.getenv('BACKUP_COMPRESS', 'true').lower() == 'true'
        
        # Criar diretório de backup se não existir
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self) -> Optional[str]:
        """Cria um backup do banco de dados"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"{self.backup_dir}/{self.db_name}_{timestamp}.sql"
            
            # Comando pg_dump
            cmd = [
                'pg_dump',
                '-h', self.db_host,
                '-U', self.db_user,
                '-d', self.db_name,
                '-F', 'c',  # Formato custom
                '-f', backup_file
            ]
            
            # Executar backup
            logger.info(f"Iniciando backup do banco {self.db_name}")
            subprocess.run(cmd, check=True)
            
            # Comprimir se necessário
            if self.compress:
                compressed_file = f"{backup_file}.gz"
                subprocess.run(['gzip', backup_file], check=True)
                backup_file = compressed_file
            
            logger.info(f"Backup criado com sucesso: {backup_file}")
            return backup_file
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao criar backup: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return None
    
    def upload_to_s3(self, backup_file: str) -> bool:
        """Faz upload do backup para o S3"""
        if not self.s3_bucket:
            logger.warning("Bucket S3 não configurado, pulando upload")
            return True
            
        try:
            s3_client = boto3.client('s3')
            file_name = os.path.basename(backup_file)
            
            logger.info(f"Fazendo upload do arquivo {file_name} para S3")
            s3_client.upload_file(
                backup_file,
                self.s3_bucket,
                f"database_backups/{file_name}"
            )
            
            logger.info("Upload concluído com sucesso")
            return True
            
        except ClientError as e:
            logger.error(f"Erro ao fazer upload para S3: {str(e)}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups antigos"""
        try:
            current_time = datetime.datetime.now()
            
            # Listar arquivos no diretório de backup
            for filename in os.listdir(self.backup_dir):
                file_path = os.path.join(self.backup_dir, filename)
                
                # Verificar idade do arquivo
                file_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                age_days = (current_time - file_time).days
                
                # Remover se mais antigo que retention_days
                if age_days > self.retention_days:
                    logger.info(f"Removendo backup antigo: {filename}")
                    os.remove(file_path)
            
            logger.info("Limpeza de backups antigos concluída")
            
        except Exception as e:
            logger.error(f"Erro ao limpar backups antigos: {str(e)}")
    
    def run(self):
        """Executa o processo completo de backup"""
        try:
            # Criar backup
            backup_file = self.create_backup()
            if not backup_file:
                return False
            
            # Upload para S3
            if not self.upload_to_s3(backup_file):
                return False
            
            # Limpar backups antigos
            self.cleanup_old_backups()
            
            logger.info("Processo de backup concluído com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante o processo de backup: {str(e)}")
            return False

if __name__ == '__main__':
    backup = DatabaseBackup()
    success = backup.run()
    sys.exit(0 if success else 1) 