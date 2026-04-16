# Código do scraper com filtro 2025
import time
import pandas as pd
from google_play_scraper import reviews, Sort


# Defini a lista de app a ser buscada
APPS_BANCOS = {
    "Nubank": "com.nu.production",
    "Itau": "com.itau",
    "Banco do Brasil": "br.com.bb.android",
    "Caixa": "br.com.gabba.Caixa",
    "Inter": "br.com.intermedium",
    "Santander": "com.santander.app",
    "Bradesco": "com.bradesco",
}

# Parametros específicos de configuração
LANG = "pt_BR"
COUNTRY = "br"
SORT = Sort.NEWEST
REVIEWS_POR_APP = 1000
SALVAR_COMO = "data/raw/reviews_bancos_playstore_2025.csv"
PAUSA_ENTRE_APPS = 2



# Função para coletar os comentários
def coletar_reviews_app(app_nome, app_id, total_desejado=1000):
    """
    Coleta reviews de um aplicativo da Play Store, filtrando apenas comentários do ano de 2025.

    A função faz a coleta paginada das reviews do app informado, ordenadas das mais recentes
    para as mais antigas. Durante a coleta:

    - ignora reviews com data inválida;
    - ignora reviews de 2026 ou posteriores;
    - armazena apenas reviews de 2025;
    - encerra a coleta ao encontrar reviews de 2024 ou anteriores;
    - encerra também se não houver mais páginas ou se ocorrer erro.

    Parâmetros
    ----------
    app_nome : str
        Nome do aplicativo ou banco, usado para identificação nos resultados.
    app_id : str
        Identificador do aplicativo na Play Store.
    total_desejado : int, opcional
        Quantidade máxima de reviews de 2025 a coletar.

    Retorna
    -------
    list[dict]
        Lista de dicionários, em que cada dicionário representa uma review coletada
        com os campos estruturados para posterior conversão em DataFrame.

    Exemplo
    -------
    >>> reviews_nubank = coletar_reviews_app("Nubank", "com.nu.production", 500)
    >>> len(reviews_nubank)
    500
    
    """

    todas_reviews = []
    continuation_token = None

    while len(todas_reviews) < total_desejado:
        restante = total_desejado - len(todas_reviews)
        lote = min(200, restante)

        try:
            resultado, continuation_token = reviews(
                app_id,
                lang=LANG,
                country=COUNTRY,
                sort=SORT,
                count=lote,
                continuation_token=continuation_token,
            )
        except Exception as e:
            print(f"[ERRO] {app_nome} ({app_id}): {e}")
            break

        if not resultado:
            print(f"[INFO] Sem mais reviews para {app_nome}.")
            break

        parar = False

        for r in resultado:
            data_review = pd.to_datetime(r.get("at"), errors="coerce")

            if pd.isna(data_review):
                continue

            # Ignora qualquer comentário após 2025
            if data_review.year > 2025:
                continue

            # Guarda apenas comentários de 2025
            if data_review.year == 2025:
                todas_reviews.append({
                    "banco": app_nome,
                    "app_id": app_id,
                    "review_id": r.get("reviewId"),
                    "score": r.get("score"),
                    "comentario": r.get("content"),
                    "data_review": data_review,
                    "versao_app_review": r.get("reviewCreatedVersion"),
                    "curtidas_review": r.get("thumbsUpCount"),
                    "url_app": f"https://play.google.com/store/apps/details?id={app_id}",
                })

            # Quando chegar em 2024 ou anterior encerra
            elif data_review.year < 2025:
                parar = True
                break

        print(f"[OK] {app_nome}: {len(todas_reviews)} reviews de 2025 coletadas até agora.")

        if parar:
            print(f"[INFO] Encontrou reviews anteriores a 2025 em {app_nome}. Encerrando coleta.")
            break

        if continuation_token is None:
            print(f"[INFO] Paginação encerrada para {app_nome}.")
            break

    return todas_reviews

# Função principal
def main():
    """
    Executa o fluxo principal de coleta de reviews dos aplicativos bancários.

    Para cada aplicativo definido em APPS_BANCOS, a função:
    - chama a rotina de coleta filtrando apenas reviews de 2025;
    - acumula os resultados em uma lista única;
    - aguarda um intervalo entre os apps para evitar excesso de requisições.

    Ao final, a função:
    - cria um DataFrame com todas as reviews coletadas;
    - remove registros duplicados;
    - garante que apenas reviews de 2025 permaneçam no resultado;
    - ordena os dados por banco e data;
    - salva o arquivo final em formato CSV.

    Caso nenhuma review de 2025 seja encontrada, a função encerra sem gerar arquivo.
    
    """
    todas = []

    for banco, app_id in APPS_BANCOS.items():
        print("=" * 70)
        print(f"Coletando reviews de: {banco} | {app_id}")

        reviews_app = coletar_reviews_app(
            app_nome=banco,
            app_id=app_id,
            total_desejado=REVIEWS_POR_APP
        )

        todas.extend(reviews_app)
        time.sleep(PAUSA_ENTRE_APPS)

    if not todas:
        print("[AVISO] Nenhuma review de 2025 foi coletada.")
        return

    df = pd.DataFrame(todas)

    # Remove duplicatas
    if "review_id" in df.columns:
        df = df.drop_duplicates(subset=["review_id"])

    # Garante novamente apenas 2025
    df["data_review"] = pd.to_datetime(df["data_review"], errors="coerce")
    df = df[df["data_review"].dt.year == 2025]

    # Ordena
    df = df.sort_values(by=["banco", "data_review"], ascending=[True, False])

    # Salva o arquivo
    df.to_csv(SALVAR_COMO, index=False, encoding="utf-8-sig")

    print("=" * 70)
    print(f"Arquivo salvo com sucesso: {SALVAR_COMO}")
    print(f"Total de reviews de 2025: {len(df)}")
    print("\nContagem por banco:")
    print(df["banco"].value_counts())

    print("\nAnos encontrados no arquivo final:")
    print(df["data_review"].dt.year.value_counts())

if __name__ == "__main__":
    main()