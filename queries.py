# SELECT
# -- Lan Credito
select_query_LanCredito = '''
    select
        'Crédito' as [Deb/Cred]
        , -sum(ctlancto.vlor_lan) as [Valor]
        , geempre.nome_emp as [Empresa]
        , ctlancto.codi_emp as [Cód. Empresa]
        , ctlancto.data_lan as [Data Lançamento]
        , ctlancto.ccre_lan as [Cód. Conta]
        , ctlancto.orig_lan as [Origem Lançamento]
    from bethadba.ctlancto with(nolock)
    inner join bethadba.geempre with(nolock) on ctlancto.codi_emp = geempre.codi_emp
    where ctlancto.ccre_lan <> 0
        and year(ctlancto.data_lan) >= year(getdate())-5
        and year(ctlancto.data_lan) <= year(getdate())
        and geempre.ucta_emp = 1
        and geempre.uefi_emp = 1
        -- and ctlancto.codi_emp = 1200 -- filtro de empresa
    group by 
        geempre.nome_emp
        , ctlancto.codi_emp 
        , ctlancto.data_lan 
        , ctlancto.ccre_lan  
        , ctlancto.orig_lan
    '''
# -- Lan Débito
select_query_LanDebito = '''
    select 
        'Débito' as [Deb/Cred]
        , sum(ctlancto.vlor_lan) as [Valor]
        , geempre.nome_emp as [Empresa]
        , ctlancto.codi_emp as [Cód. Empresa]
        , ctlancto.data_lan as [Data Lançamento]
        , ctlancto.cdeb_lan as [Cód. Conta]
        , ctlancto.orig_lan as [Origem Lançamento]
    from bethadba.ctlancto with(nolock)
    inner join bethadba.geempre with(nolock) on ctlancto.codi_emp = geempre.codi_emp
    where ctlancto.cdeb_lan <> 0
        and year(ctlancto.data_lan) >= year(getdate())-5
        and year(ctlancto.data_lan) <= year(getdate())
        and geempre.ucta_emp = 1
        and geempre.uefi_emp = 1
        -- and ctlancto.codi_emp = 1200 -- filtro de empresa
    group by geempre.nome_emp
        , ctlancto.codi_emp 
        , ctlancto.data_lan
        , ctlancto.cdeb_lan 
        , ctlancto.orig_lan 
    '''

# -- Acumuladores
select_query_Acumuladores = '''
    select codi_emp as [Cód. Empresa]
        , codi_acu as [Cód. Acumulador]
        , nome_acu as [Acumulador]
        , descricao_acu as [Descrição Acumulador]
        , cdeb_acu as [Cód. Conta Contábil] 
    from bethadba.EFACUMULADORES with(nolock)
    where cdeb_acu <> 0
        -- and codi_emp = 1200 -- filtro de empresa

    union all

    select codi_emp as [Cód. Empresa]
        , codi_acu as [Cód. Acumulador]
        , nome_acu as [Acumulador]
        , descricao_acu as [Descrição Acumulador]
        , ccre_acu as [Cód. Conta Contábil]
    from bethadba.EFACUMULADORES with(nolock)
    where ccre_acu <> 0    
        -- and codi_emp = 1200 -- filtro de empresa
    '''
    
# -- LanFisImpostosEntradas
select_query_LanFisImpostosEntradas = '''
    SELECT 'Entrada' as Tipo
        , g.nome_emp as [Empresa]
        , n.codi_emp as [Cód. Empresa]
        , n.dent_ent as [Data Lançamento]
        , n.codi_acu as [Cód. Acumulador]
        , -I.Vlor_IEN as [Valor Temp]
    FROM BETHADBA.EFIMPENT AS I 
    INNER JOIN BETHADBA.EFENTRADAS AS N ON I.CODI_EMP = N.CODI_EMP AND I.CODI_ENT = N.CODI_ENT  
    INNER JOIN BETHADBA.GEEMPRE AS G ON G.CODI_EMP = N.CODI_EMP 
    WHERE I.VLOR_IEN > 0
        and year(n.dent_ent) >= year(getdate())-1
        and year(n.dent_ent) <= year(getdate())
        and n.codi_acu > 0
        and g.ucta_emp = 1
        and g.uefi_emp = 1
        and i.codi_imp not in (16, 18, 25, 26, 27)
        -- and n.codi_emp = 1200 -- filtro de empresa
        and exists (
            SELECT 
                TOP 1 1 
            FROM bethadba.EFACUMULADOR_VIGENCIA AS ACV with(nolock)
            WHERE ACV.CODI_ACU = n.CODI_ACU
                AND ACV.CODI_EMP = n.CODI_EMP
                AND (
                    isnull(ACV.CT_DESCONTO,0)
                    +isnull(ACV.CT_ACRESCIMO,0)
                    +isnull(ACV.CT_FRETE,0)
                    +isnull(ACV.CT_SEGURO,0)
                    +isnull(ACV.CT_DESPESAS_ACESSORIAS,0)
                    +isnull(ACV.CT_PEDAGIO,0)
                    +isnull(ACV.CT_IPI_ENTRADA,0)
                    +isnull(ACV.CT_ICMS_ST_ENTRADA,0)
                ) > 0)
    '''

# -- LanFisImpostosSaidas
select_query_LanFisImpostosSaidas = '''
    SELECT 'Saida' as Tipo
        , g.nome_emp as [Empresa]
        , n.codi_emp as [Cód. Empresa]
        , n.dsai_sai as [Data Lançamento]
        , n.codi_acu as [Cód. Acumulador]
        , -I.Vlor_Isa as [Valor Temp]
    FROM BETHADBA.EFIMPsai  AS I
    INNER JOIN BETHADBA.EFsaidas AS N ON I.CODI_EMP = N.CODI_EMP AND I.CODI_sai = N.CODI_sai  
    INNER JOIN BETHADBA.GEEMPRE AS G  ON G.CODI_EMP = N.CODI_EMP 
    WHERE I.VLOR_Isa > 0
        and year(n.dsai_sai) >= year(getdate())-1
        and year(n.dsai_sai) <= year(getdate())
        and n.codi_acu > 0
        and g.ucta_emp = 1
        and g.uefi_emp = 1
        and i.codi_imp not in (1, 28)
        -- and n.codi_emp = 1200 -- filtro de empresa
        and exists (
            SELECT 
                TOP 1 1 
            FROM bethadba.EFACUMULADOR_VIGENCIA AS ACV with(nolock)
            WHERE ACV.CODI_ACU = n.CODI_ACU
                AND ACV.CODI_EMP = n.CODI_EMP
                AND (
                    isnull(ACV.CT_DESCONTO,0)
                    +isnull(ACV.CT_ACRESCIMO,0)
                    +isnull(ACV.CT_FRETE,0)
                    +isnull(ACV.CT_SEGURO,0)
                    +isnull(ACV.CT_DESPESAS_ACESSORIAS,0)
                    +isnull(ACV.CT_PEDAGIO,0)
                    +isnull(ACV.CT_IPI_ENTRADA,0)
                    +isnull(ACV.CT_ICMS_ST_ENTRADA,0)
                ) > 0)
    '''

# -- LanFisImpostosServicos
select_query_LanFisImpostosServicos = '''
    SELECT 'Servicos' as Tipo
        , g.nome_emp as [Empresa]
        , n.codi_emp as [Cód. Empresa]
        , n.dser_ser as [Data Lançamento]
        , n.codi_acu as [Cód. Acumulador]
        , -I.Vlor_Ise as [Valor Temp]
    FROM BETHADBA.EFIMPser AS I 
    INNER JOIN BETHADBA.EFservicos AS N ON I.CODI_EMP = N.CODI_EMP AND I.CODI_ser = N.CODI_ser  
    INNER JOIN BETHADBA.GEEMPRE AS G ON G.CODI_EMP = N.CODI_EMP 
    WHERE I.VLOR_Ise > 0
        and year(n.dser_ser) >= year(getdate())-1
        and year(n.dser_ser) <= year(getdate())
        and n.codi_acu > 0
        and g.ucta_emp = 1
        and g.uefi_emp = 1
        -- and n.codi_emp = 1200 -- filtro de empresa
        and exists (
            SELECT 
                TOP 1 1 
            FROM bethadba.EFACUMULADOR_VIGENCIA AS ACV with(nolock)
            WHERE ACV.CODI_ACU = n.CODI_ACU
                AND ACV.CODI_EMP = n.CODI_EMP
                AND (
                    isnull(ACV.CT_DESCONTO,0)
                    +isnull(ACV.CT_ACRESCIMO,0)
                    +isnull(ACV.CT_FRETE,0)
                    +isnull(ACV.CT_SEGURO,0)
                    +isnull(ACV.CT_DESPESAS_ACESSORIAS,0)
                    +isnull(ACV.CT_PEDAGIO,0)
                    +isnull(ACV.CT_IPI_ENTRADA,0)
                    +isnull(ACV.CT_ICMS_ST_ENTRADA,0)
                ) > 0)
    '''

# -- FisAcumuladores
select_query_FisAcumuladores = '''
    select
        'Débito' as [Deb/Cred] 
        , codi_emp as [Cód. Empresa]
        , codi_acu as [Cód. Acumulador]
        , nome_acu as [Acumulador]
        , descricao_acu as [Descrição Acumulador]
        , cdeb_acu as [Cód. Conta Contábil] 
    from bethadba.EFACUMULADORES with(nolock)
    where cdeb_acu > 0
        -- and codi_emp = 1200 -- filtro de empresa

        union all

    select 
        'Crédito'  as [Deb/Cred] 
        , codi_emp as [Cód. Empresa]
        , codi_acu as [Cód. Acumulador]
        , nome_acu as [Acumulador]
        , descricao_acu as [Descrição Acumulador]
        , ccre_acu as [Cód. Conta Contábil]
    from bethadba.EFACUMULADORES with(nolock)
    where ccre_acu > 0
        -- and codi_emp = 1200 -- filtro de empresa
    '''

# -- LanFisEntradas
select_query_LanFisEntradas = '''
    select 'Entrada' as Tipo
        , geempre.nome_emp as [Empresa]
        , efentradas.codi_emp as [Cód. Empresa]
        , efentradas.dent_ent as [Data Lançamento]
        , efentradas.codi_acu as [Cód. Acumulador]
        , sum(efentradas.vcon_ent) as [Valor Temp]
    from bethadba.efentradas with(nolock)
    inner join bethadba.geempre with(nolock) on efentradas.codi_emp = geempre.codi_emp
    where year(efentradas.dent_ent) >= year(getdate())-1
        and year(efentradas.dent_ent) <= year(getdate())
        and efentradas.codi_acu > 0
        and geempre.ucta_emp = 1
        and geempre.uefi_emp = 1
        -- and efentradas.codi_emp = 1200 -- filtro de empresa
        and exists (
            SELECT 
                TOP 1 1 
            FROM bethadba.EFACUMULADOR_VIGENCIA AS ACV with(nolock)
            WHERE ACV.CODI_ACU = efentradas.CODI_ACU
                AND ACV.CODI_EMP = efentradas.CODI_EMP
                AND (
                    isnull(ACV.CT_DESCONTO,0)
                    +isnull(ACV.CT_ACRESCIMO,0)
                    +isnull(ACV.CT_FRETE,0)
                    +isnull(ACV.CT_SEGURO,0)
                    +isnull(ACV.CT_DESPESAS_ACESSORIAS,0)
                    +isnull(ACV.CT_PEDAGIO,0)
                    +isnull(ACV.CT_IPI_ENTRADA,0)
                    +isnull(ACV.CT_ICMS_ST_ENTRADA,0)
                ) > 0)
    group by 
        geempre.nome_emp
        , efentradas.codi_emp
        , efentradas.dent_ent
        , efentradas.codi_acu
    '''

# -- LanFisSaidas
select_query_LanFisSaidas = '''
    select
        'Saida' as Tipo
        , geempre.nome_emp as [Empresa]
        , efsaidas.codi_emp as [Cód. Empresa]
        , efsaidas.dsai_sai as [Data Lançamento]
        , efsaidas.codi_acu as [Cód. Acumulador]
        , sum(efsaidas.vcon_sai) as [Valor Temp]
    from bethadba.efsaidas with(nolock)
    inner join bethadba.geempre with(nolock) on efsaidas.codi_emp = geempre.codi_emp
    where year(efsaidas.dsai_sai) >= year(getdate())-1
        and year(efsaidas.dsai_sai) <= year(getdate())
        and efsaidas.codi_acu > 0
        and geempre.ucta_emp = 1
        and geempre.uefi_emp = 1
        -- and efsaidas.codi_emp = 1200 -- filtro de empresa
        and exists (
            SELECT 
                TOP 1 1 
            FROM bethadba.EFACUMULADOR_VIGENCIA AS ACV with(nolock)
            WHERE ACV.CODI_ACU = efsaidas.CODI_ACU
                AND ACV.CODI_EMP = efsaidas.CODI_EMP
                AND (
                    isnull(ACV.CT_DESCONTO,0)
                    +isnull(ACV.CT_ACRESCIMO,0)
                    +isnull(ACV.CT_FRETE,0)
                    +isnull(ACV.CT_SEGURO,0)
                    +isnull(ACV.CT_DESPESAS_ACESSORIAS,0)
                    +isnull(ACV.CT_PEDAGIO,0)
                    +isnull(ACV.CT_IPI_ENTRADA,0)
                    +isnull(ACV.CT_ICMS_ST_ENTRADA,0)
                ) > 0)
    group by 
        geempre.nome_emp
        , efsaidas.codi_emp
        , efsaidas.dsai_sai
        , efsaidas.codi_acu    
    '''

# -- LanFisServicos
select_query_LanFisServicos = '''
    select
        'Servicos' as Tipo
        , geempre.nome_emp as [Empresa]
        , efservicos.codi_emp as [Cód. Empresa]
        , efservicos.dser_ser as [Data Lançamento]
        , efservicos.codi_acu as [Cód. Acumulador]
        , sum(efservicos.vcon_ser) as [Valor Temp]
    from bethadba.efservicos with(nolock)
    inner join bethadba.geempre with(nolock) on efservicos.codi_emp = geempre.codi_emp
    where year(efservicos.dser_ser) >= year(getdate())-1
        and year(efservicos.dser_ser) <= year(getdate())
        and efservicos.codi_acu > 0
        and geempre.ucta_emp = 1
        and geempre.uefi_emp = 1
        -- and efservicos.codi_emp = 1200 -- filtro de empresa
        and exists (
            SELECT 
                TOP 1 1 
            FROM bethadba.EFACUMULADOR_VIGENCIA AS ACV with(nolock)
            WHERE ACV.CODI_ACU = efservicos.CODI_ACU
                AND ACV.CODI_EMP = efservicos.CODI_EMP
                AND (
                    isnull(ACV.CT_DESCONTO,0)
                    +isnull(ACV.CT_ACRESCIMO,0)
                    +isnull(ACV.CT_FRETE,0)
                    +isnull(ACV.CT_SEGURO,0)
                    +isnull(ACV.CT_DESPESAS_ACESSORIAS,0)
                    +isnull(ACV.CT_PEDAGIO,0)
                    +isnull(ACV.CT_IPI_ENTRADA,0)
                    +isnull(ACV.CT_ICMS_ST_ENTRADA,0)
                ) > 0)
    group by 
        geempre.nome_emp
        , efservicos.codi_emp
        , efservicos.dser_ser
        , efservicos.codi_acu
    '''
    
# UPSERT
# -- Lan Credito
upsert_query_LanCredito = '''
    INSERT INTO LanCredito
        ("Deb/Cred", Valor, Empresa, "Cód. Empresa", "Cód. Conta", "Origem Lançamento", "Data Lançamento")
    VALUES
        (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT ("Cód. Empresa", "Cód. Conta", "Origem Lançamento", "Data Lançamento") DO 
        UPDATE SET
            "Deb/Cred" = excluded."Deb/Cred",
            Valor = excluded.Valor,
            Empresa = excluded.Empresa
    '''
# -- Lan Débito
upsert_query_LanDebito = '''
    INSERT INTO LanDebito
        ("Deb/Cred", Valor, Empresa, "Cód. Empresa", "Cód. Conta", "Origem Lançamento", "Data Lançamento")
    VALUES
        (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT ("Cód. Empresa", "Cód. Conta", "Origem Lançamento", "Data Lançamento") DO 
        UPDATE SET
            "Deb/Cred" = excluded."Deb/Cred",
            Valor = excluded.Valor,
            Empresa = excluded.Empresa
    '''

# -- Acumuladores
upsert_query_Acumuladores = '''
    INSERT INTO Acumuladores
        ("Cód. Empresa", "Cód. Acumulador", Acumulador, "Descrição Acumulador", "Cód. Conta Contábil")
    VALUES
        (?, ?, ?, ?, ?)
    ON CONFLICT ("Cód. Empresa", "Cód. Acumulador", "Cód. Conta Contábil") DO 
        UPDATE SET
            Acumulador = excluded.Acumulador,
            "Descrição Acumulador" = excluded."Descrição Acumulador"
    '''
    
# -- LanFisImpostosEntradas
upsert_query_LanFisImpostosEntradas = '''
    INSERT INTO LanFisImpostosEntradas
    (Tipo, Empresa, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp")
    VALUES
        (?, ?, ?, ?, ?, ?)
    ON CONFLICT (Tipo, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp") DO 
        UPDATE SET
            "Valor Temp" = excluded."Valor Temp", 
            Empresa = excluded.Empresa
    '''

# -- LanFisImpostosSaidas
upsert_query_LanFisImpostosSaidas = '''
    INSERT INTO LanFisImpostosSaidas
    (Tipo, Empresa, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp")
    VALUES
        (?, ?, ?, ?, ?, ?)
    ON CONFLICT (Tipo, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp") DO 
        UPDATE SET
            "Valor Temp" = excluded."Valor Temp", 
            Empresa = excluded.Empresa
    '''

# -- LanFisImpostosServicos
upsert_query_LanFisImpostosServicos = '''
    INSERT INTO LanFisImpostosServicos
    (Tipo, Empresa, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp")
    VALUES
        (?, ?, ?, ?, ?, ?)
    ON CONFLICT (Tipo, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp") DO 
        UPDATE SET
            "Valor Temp" = excluded."Valor Temp"
    '''

# -- FisAcumuladores
upsert_query_FisAcumuladores = '''
    INSERT INTO FisAcumuladores
    ("Deb/Cred", "Cód. Empresa", "Cód. Acumulador", Acumulador, "Descrição Acumulador", "Cód. Conta Contábil", CodiPlan, "Contas.NomeConta", "Contas.ClassificacaoConta", "Contas.TipoConta", "Contas.origem_reg", "Contas.DataConta", "Contas.SituacaoConta")
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT ("Deb/Cred", "Cód. Empresa", "Cód. Acumulador", "Cód. Conta Contábil", CodiPlan, "Contas.ClassificacaoConta", "Contas.origem_reg") DO
        UPDATE SET
            Acumulador = excluded.Acumulador,
            "Descrição Acumulador" = excluded."Descrição Acumulador",
            "Contas.NomeConta" = excluded."Contas.NomeConta",
            "Contas.TipoConta" = excluded."Contas.TipoConta",
            "Contas.DataConta" = excluded."Contas.DataConta",
            "Contas.SituacaoConta" = excluded."Contas.SituacaoConta"
    '''

# -- LanFisEntradas
upsert_query_LanFisEntradas = '''
    INSERT INTO LanFisEntradas
    (Tipo, Empresa, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp")
    VALUES
        (?, ?, ?, ?, ?, ?)
    ON CONFLICT (Tipo, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador") DO 
        UPDATE SET
            "Valor Temp" = excluded."Valor Temp"
    '''

# -- LanFisSaidas
upsert_query_LanFisSaidas = '''
    INSERT INTO LanFisSaidas
    (Tipo, Empresa, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp")
    VALUES
        (?, ?, ?, ?, ?, ?)
    ON CONFLICT (Tipo, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador") DO 
        UPDATE SET
            "Valor Temp" = excluded."Valor Temp"
    '''

# -- LanFisServicos
upsert_query_LanFisServicos = '''
    INSERT INTO LanFisServicos
    (Tipo, Empresa, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador", "Valor Temp")
    VALUES
        (?, ?, ?, ?, ?, ?)
    ON CONFLICT (Tipo, "Cód. Empresa", "Data Lançamento", "Cód. Acumulador") DO 
        UPDATE SET
            "Valor Temp" = excluded."Valor Temp"
    '''


# CREATE
# -- Lan Credito
create_query_LanCredito = '''
    -- LanCredito definition

    CREATE TABLE IF NOT EXISTS LanCredito (
        "Deb/Cred" VARCHAR(50),
        Valor VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Cód. Conta" INTEGER,
        "Origem Lançamento" INTEGER,
        "Data Lançamento" VARCHAR(50)
    );
    '''
    
# -- Lan Débito
create_query_LanDebito = '''
    -- LanDebito definition

    CREATE TABLE IF NOT EXISTS LanDebito (
        "Deb/Cred" VARCHAR(50),
        Valor VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Cód. Conta" INTEGER,
        "Origem Lançamento" INTEGER,
        "Data Lançamento" VARCHAR(50)
    );
    '''

# -- Acumuladores
create_query_Acumuladores = '''
    -- Acumuladores definition

    CREATE TABLE IF NOT EXISTS Acumuladores (
        "Cód. Empresa" INTEGER,
        "Cód. Acumulador" INTEGER,
        Acumulador VARCHAR(50),
        "Descrição Acumulador" VARCHAR(50),
        "Cód. Conta Contábil" INTEGER
    );
    '''
    
# -- LanFisImpostosEntradas
create_query_LanFisImpostosEntradas = '''
-- LanFisImpostosEntradas definition

    CREATE TABLE IF NOT EXISTS LanFisImpostosEntradas (
        Tipo VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Data Lançamento" VARCHAR(50),
        "Cód. Acumulador" INTEGER,
        "Valor Temp" VARCHAR(50)
    );
    '''

# -- LanFisImpostosSaidas
create_query_LanFisImpostosSaidas = '''
    -- LanFisImpostosSaidas definition

    CREATE TABLE IF NOT EXISTS LanFisImpostosSaidas (
        Tipo VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Data Lançamento" VARCHAR(50),
        "Cód. Acumulador" INTEGER,
        "Valor Temp" VARCHAR(50)
    );
    '''

# -- LanFisImpostosServicos
create_query_LanFisImpostosServicos = '''
    -- LanFisImpostosServicos definition

    CREATE TABLE IF NOT EXISTS LanFisImpostosServicos (
        Tipo VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Data Lançamento" VARCHAR(50),
        "Cód. Acumulador" INTEGER,
        "Valor Temp" VARCHAR(50)
    );
    '''

# -- FisAcumuladores
create_query_FisAcumuladores = '''
    -- FisAcumuladores definition

    CREATE TABLE IF NOT EXISTS FisAcumuladores (
        "Deb/Cred" VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Cód. Acumulador" INTEGER,
        Acumulador VARCHAR(50),
        "Descrição Acumulador" VARCHAR(50),
        "Cód. Conta Contábil" INTEGER,
        CodiPlan INTEGER,
        "Contas.NomeConta" VARCHAR(50),
        "Contas.ClassificacaoConta" INTEGER,
        "Contas.TipoConta" VARCHAR(50),
        "Contas.origem_reg" INTEGER,
        "Contas.DataConta" VARCHAR(50),
        "Contas.SituacaoConta" VARCHAR(50)
    );
    '''

# -- LanFisEntradas
create_query_LanFisEntradas = '''
    -- LanFisEntradas definition

    CREATE TABLE IF NOT EXISTS LanFisEntradas (
        Tipo VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Cód. Acumulador" INTEGER,
        "Valor Temp" VARCHAR(50),
        "Data Lançamento" VARCHAR(50)
    );
    '''

# -- LanFisSaidas
create_query_LanFisSaidas = '''
    -- LanFisSaidas definition

    CREATE TABLE IF NOT EXISTS LanFisSaidas (
        Tipo VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Cód. Acumulador" INTEGER,
        "Valor Temp" VARCHAR(50),
        "Data Lançamento" VARCHAR(50)
    );
    '''

# -- LanFisServicos
create_query_LanFisServicos = '''
    -- LanFisServicos definition

    CREATE TABLE IF NOT EXISTS LanFisServicos (
        Tipo VARCHAR(50),
        Empresa VARCHAR(50),
        "Cód. Empresa" INTEGER,
        "Cód. Acumulador" INTEGER,
        "Valor Temp" INTEGER,
        "Data Lançamento" VARCHAR(50)
    );
    '''