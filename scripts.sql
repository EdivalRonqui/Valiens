-- Lan Credito
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

-- Lan Débito
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

-- Acumuladores
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

-- LanFisImpostosEntradas
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

-- LanFisImpostosSaidas
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

-- LanFisImpostosServicos
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

-- FisAcumuladores
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

-- LanFisEntradas
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

-- LanFisSaidas
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

-- LanFisServicos
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

