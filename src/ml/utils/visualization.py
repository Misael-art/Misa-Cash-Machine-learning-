"""
Módulo para visualização de resultados de modelos de predição de despesas.

Este módulo fornece funções para criar gráficos e visualizações que ajudam
a analisar e interpretar os resultados dos modelos de predição de despesas.
Contém funções para visualizar predições, erros de predição, importância
de features e outras métricas relevantes.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.dates as mdates
from typing import List, Dict, Tuple, Optional, Union


def plot_predictions_vs_actual(
    dates: pd.Series,
    actual: pd.Series,
    predicted: pd.Series,
    title: str = "Valores Previstos vs. Reais",
    figsize: Tuple[int, int] = (12, 6),
    confidence_intervals: Optional[Tuple[pd.Series, pd.Series]] = None
) -> plt.Figure:
    """
    Plota valores previstos contra valores reais ao longo do tempo.

    Args:
        dates: Série com as datas para o eixo x
        actual: Série com os valores reais
        predicted: Série com os valores previstos
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)
        confidence_intervals: Tupla opcional com os limites inferior e superior do intervalo de confiança

    Returns:
        Objeto Figure do matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plotar valores reais e previstos
    ax.plot(dates, actual, 'o-', label='Valores Reais', alpha=0.7)
    ax.plot(dates, predicted, 's-', label='Valores Previstos', alpha=0.7)
    
    # Adicionar intervalos de confiança se fornecidos
    if confidence_intervals is not None:
        lower_bound, upper_bound = confidence_intervals
        ax.fill_between(dates, lower_bound, upper_bound, alpha=0.2, color='blue',
                         label='Intervalo de Confiança (95%)')
    
    # Formatação do gráfico
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Valor da Despesa', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Formatação do eixo de datas
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    fig.tight_layout()
    return fig


def plot_prediction_error(
    dates: pd.Series,
    errors: pd.Series,
    title: str = "Erro de Predição ao Longo do Tempo",
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Plota o erro de predição ao longo do tempo.

    Args:
        dates: Série com as datas para o eixo x
        errors: Série com os erros de predição (atual - previsto)
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)

    Returns:
        Objeto Figure do matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plotar erros
    ax.bar(dates, errors, alpha=0.7, color='royalblue')
    ax.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    
    # Adicionar média e desvio padrão do erro
    mean_error = errors.mean()
    std_error = errors.std()
    ax.axhline(y=mean_error, color='g', linestyle='--', 
               label=f'Erro Médio: {mean_error:.2f}')
    
    # Adicionar bandas de +/- 1 desvio padrão
    ax.axhline(y=mean_error + std_error, color='g', linestyle=':', alpha=0.5,
               label=f'Desvio Padrão: {std_error:.2f}')
    ax.axhline(y=mean_error - std_error, color='g', linestyle=':', alpha=0.5)
    
    # Formatação do gráfico
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Erro (Atual - Previsto)', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Formatação do eixo de datas
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    fig.tight_layout()
    return fig


def plot_feature_importance(
    feature_names: List[str],
    importance_values: List[float],
    title: str = "Importância das Features",
    figsize: Tuple[int, int] = (10, 8),
    top_n: Optional[int] = None
) -> plt.Figure:
    """
    Plota a importância das features do modelo.

    Args:
        feature_names: Lista com os nomes das features
        importance_values: Lista com os valores de importância
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)
        top_n: Opcional, número de top features para mostrar

    Returns:
        Objeto Figure do matplotlib
    """
    # Criar DataFrame para facilitar a ordenação
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importância': importance_values
    })
    
    # Ordenar por importância
    importance_df = importance_df.sort_values('Importância', ascending=False)
    
    # Limitar para as top_n features se especificado
    if top_n is not None:
        importance_df = importance_df.head(top_n)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Criar gráfico de barras horizontais
    sns.barplot(
        x='Importância',
        y='Feature',
        data=importance_df,
        ax=ax,
        palette='viridis'
    )
    
    # Formatação do gráfico
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Importância', fontsize=12)
    ax.set_ylabel('Feature', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7, axis='x')
    
    fig.tight_layout()
    return fig


def plot_error_distribution(
    errors: pd.Series,
    title: str = "Distribuição do Erro de Predição",
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Plota a distribuição dos erros de predição.

    Args:
        errors: Série com os erros de predição
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)

    Returns:
        Objeto Figure do matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plotar histograma e KDE
    sns.histplot(errors, kde=True, ax=ax, color='royalblue', alpha=0.7)
    
    # Adicionar linhas verticais para estatísticas importantes
    mean_error = errors.mean()
    median_error = errors.median()
    
    ax.axvline(x=mean_error, color='r', linestyle='--', 
               label=f'Média: {mean_error:.2f}')
    ax.axvline(x=median_error, color='g', linestyle='--', 
               label=f'Mediana: {median_error:.2f}')
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.5,
               label='Erro Zero')
    
    # Formatação do gráfico
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Erro de Predição', fontsize=12)
    ax.set_ylabel('Frequência', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    fig.tight_layout()
    return fig


def plot_metrics_comparison(
    model_names: List[str],
    metrics_dict: Dict[str, List[float]],
    title: str = "Comparação de Métricas entre Modelos",
    figsize: Tuple[int, int] = (12, 8)
) -> plt.Figure:
    """
    Plota uma comparação de diferentes métricas entre modelos.

    Args:
        model_names: Lista com os nomes dos modelos
        metrics_dict: Dicionário com as métricas (chave) e lista de valores para cada modelo
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)

    Returns:
        Objeto Figure do matplotlib
    """
    n_metrics = len(metrics_dict)
    n_models = len(model_names)
    
    fig, axes = plt.subplots(1, n_metrics, figsize=figsize)
    if n_metrics == 1:
        axes = [axes]
    
    # Para cada métrica, criar um gráfico de barras
    for i, (metric_name, metric_values) in enumerate(metrics_dict.items()):
        ax = axes[i]
        x_pos = np.arange(n_models)
        
        ax.bar(x_pos, metric_values, width=0.6, alpha=0.7)
        
        # Adicionar rótulos de valor
        for j, value in enumerate(metric_values):
            ax.text(j, value * 1.05, f'{value:.4f}', ha='center', va='bottom', 
                   fontsize=9, rotation=45 if value > 1000 else 0)
        
        # Formatação do gráfico
        ax.set_title(metric_name, fontsize=12)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(model_names, rotation=45, ha='right')
        ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    fig.suptitle(title, fontsize=14)
    fig.tight_layout()
    fig.subplots_adjust(top=0.85)
    
    return fig


def plot_seasonal_patterns(
    data: pd.DataFrame,
    date_column: str,
    value_column: str,
    period: str = 'M',
    title: str = "Padrões Sazonais",
    figsize: Tuple[int, int] = (12, 8)
) -> plt.Figure:
    """
    Plota padrões sazonais nos dados (mensal, trimestral, etc.).

    Args:
        data: DataFrame com os dados
        date_column: Nome da coluna de data
        value_column: Nome da coluna de valor
        period: Período para agrupamento ('M' para mensal, 'Q' para trimestral, etc.)
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)

    Returns:
        Objeto Figure do matplotlib
    """
    # Garantir que a coluna de data está no formato correto
    df = data.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Extrair componentes de data
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['quarter'] = df[date_column].dt.quarter
    
    fig, axes = plt.subplots(2, 1, figsize=figsize)
    
    # Gráfico de médias mensais
    monthly_avg = df.groupby('month')[value_column].mean()
    axes[0].plot(monthly_avg.index, monthly_avg.values, 'o-', linewidth=2, markersize=8)
    axes[0].set_title('Média Mensal', fontsize=12)
    axes[0].set_xticks(range(1, 13))
    axes[0].set_xticklabels(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                           'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    axes[0].grid(True, linestyle='--', alpha=0.7)
    
    # Gráfico de médias trimestrais
    quarterly_avg = df.groupby('quarter')[value_column].mean()
    axes[1].plot(quarterly_avg.index, quarterly_avg.values, 's-', linewidth=2, markersize=8, color='green')
    axes[1].set_title('Média Trimestral', fontsize=12)
    axes[1].set_xticks(range(1, 5))
    axes[1].set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    axes[1].grid(True, linestyle='--', alpha=0.7)
    
    # Formatação geral
    fig.suptitle(title, fontsize=14)
    for ax in axes:
        ax.set_ylabel(value_column, fontsize=10)
    
    fig.tight_layout()
    fig.subplots_adjust(top=0.9)
    
    return fig


def plot_forecast_horizon(
    actual: pd.Series,
    forecasts: Dict[str, pd.Series],
    dates: pd.Series,
    title: str = "Previsões para Diferentes Horizontes",
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Plota múltiplas previsões para diferentes horizontes de tempo.

    Args:
        actual: Série com os valores reais
        forecasts: Dicionário com horizonte de previsão como chave e série de previsões como valor
        dates: Série com as datas para o eixo x
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)

    Returns:
        Objeto Figure do matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plotar valores reais
    ax.plot(dates, actual, 'o-', label='Valores Reais', linewidth=2)
    
    # Plotar cada horizonte de previsão
    colors = plt.cm.viridis(np.linspace(0, 1, len(forecasts)))
    
    for i, (horizon, forecast) in enumerate(forecasts.items()):
        ax.plot(dates, forecast, 's-', alpha=0.7, linewidth=1.5, 
                label=f'Previsão - {horizon}', color=colors[i])
    
    # Formatação do gráfico
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Valor da Despesa', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Formatação do eixo de datas
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    fig.tight_layout()
    return fig


def create_performance_summary(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> pd.DataFrame:
    """
    Cria um resumo de métricas de performance do modelo.

    Args:
        y_true: Array com os valores reais
        y_pred: Array com os valores previstos

    Returns:
        DataFrame com as métricas de performance
    """
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # Calcular erro percentual médio absoluto (MAPE)
    mape = np.mean(np.abs((y_true - y_pred) / np.maximum(1e-10, np.abs(y_true)))) * 100
    
    # Calcular estatísticas dos erros
    errors = y_true - y_pred
    mean_error = np.mean(errors)
    median_error = np.median(errors)
    std_error = np.std(errors)
    
    # Criar DataFrame de resumo
    metrics = pd.DataFrame({
        'Métrica': ['MSE', 'RMSE', 'MAE', 'R²', 'MAPE (%)', 
                    'Erro Médio', 'Erro Mediano', 'Desvio Padrão do Erro'],
        'Valor': [mse, rmse, mae, r2, mape, mean_error, median_error, std_error]
    })
    
    return metrics


def plot_correlation_heatmap(
    data: pd.DataFrame,
    title: str = "Matriz de Correlação",
    figsize: Tuple[int, int] = (12, 10),
    mask_upper: bool = True,
    cmap: str = "coolwarm"
) -> plt.Figure:
    """
    Plota uma matriz de correlação como um heatmap.

    Args:
        data: DataFrame com os dados numéricos
        title: Título do gráfico
        figsize: Tamanho da figura (largura, altura)
        mask_upper: Se True, mascara o triângulo superior da matriz
        cmap: Mapa de cores para o heatmap

    Returns:
        Objeto Figure do matplotlib
    """
    # Calcular a matriz de correlação
    corr_matrix = data.corr()
    
    # Criar máscara para o triângulo superior
    mask = None
    if mask_upper:
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Criar heatmap
    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=cmap,
        vmax=1,
        vmin=-1,
        center=0,
        annot=True,
        fmt=".2f",
        square=True,
        linewidths=.5,
        cbar_kws={"shrink": .8},
        ax=ax
    )
    
    # Formatação do gráfico
    ax.set_title(title, fontsize=14, pad=20)
    
    fig.tight_layout()
    return fig 