----------------------------Método de pag mais usado-----------------------------

CREATE VIEW MetodoMais
AS 
SELECT metodo_pag, COUNT(metodo_pag) as total
FROM pagamento
GROUP BY metodo_pag;

----------------------------Valor medio de vendas por ano---------------------

CREATE VIEW MediaPedidosAno
AS 
SELECT
    year(dia_pedido) as ano,
    avg(total_pedido) as media
FROM pedido
GROUP BY year(dia_pedido);

-----------------------------ano e mes de maior num de vendas-------------------

CREATE VIEW MaiorVendasM_A
AS 
SELECT 
    year(dia_pedido) as ano,
    month(dia_pedido) as mes,
    count(id_pedido) as total
FROM pedido
GROUP BY ano, mes;

-----------------------cliente com compras todo mes-------------------------

delimiter //
create procedure ClienteAnual(in ano year)
begin
    select id_conta, count(distinct month(dia_pedido)) as meses
    from pedido
    where year(dia_pedido) = ano
    group by id_conta
    having meses = 12;
end //

--------------------produtos mais vendidos-------------------

CREATE VIEW ProdutoMais
AS 
SELECT 
    nome_produto,
    sum(itempedido.quanti_item) as total
from produto
join itempedido
on produto.id_produto = itempedido.id_produto
GROUP BY nome_produto;