-- ============================================================
--  ASSIGNMENT 02 — Joins
--  Database : BikeStores
-- ============================================================


-- ============================================================
--  Question 1
--  Retrieve the product_name, list_price, and category_name
--  for every product.
--  Use production.products and production.categories.
--  Sort the results by product_name ascending.
-- ============================================================

-- Write your query below:
select pro.product_name, pro.list_price, cat.category_name from production.products pro
inner join production.categories cat
on pro.category_id = cat.category_id order by pro.product_name




-- ============================================================
--  Question 2
--  Show the customer full name (as full_name), order_id,
--  and order_date for all customers who have placed an order.
--  Use sales.customers and sales.orders.
--  Sort by order_date descending.
-- ============================================================

-- Write your query below:
select cus.first_name + ' '+cus.last_name as 'full_name',ord.order_id,ord.order_date from sales.customers cus
inner join sales.orders ord
on cus.customer_id = ord.customer_id order by ord.order_date desc



-- ============================================================
--  Question 3
--  Retrieve product_name, list_price, category_name, and
--  brand_name for every product.
--  Use production.products, production.categories,
--  and production.brands.
--  Sort by brand_name then product_name (both ascending).
-- ============================================================

-- Write your query below:
select pro.product_name,pro.list_price,cat.category_name,bra.brand_name from production.products pro
inner join	production.categories cat
on cat.category_id = pro.category_id
inner join production.brands bra
on bra.brand_id = pro.brand_id
order by bra.brand_name , pro.product_name

-- ============================================================
--  Question 4
--  List all products along with their order_id and item_id.
--  Make sure products that have NEVER been ordered also appear
--  in the result (those rows will have NULL for order_id
--  and item_id).
--  Use production.products and sales.order_items.
--  Sort by order_id ascending.
-- ============================================================
	
-- Write your query below:
select pro.*, ord.order_id,ord.item_id from production.products pro
left join sales.order_items ord
on pro.product_id = ord.product_id
order by ord.order_id asc


-- ============================================================
--  Question 5
--  Using your answer from Question 4 as a base, filter the
--  results to show ONLY the products that have never been
--  ordered.
--  Display only product_id and product_name.
-- ============================================================

-- Write your query below:
 select pro.product_id,pro.product_name from production.products pro
 left join sales.order_items sal
 on pro.product_id=sal.product_id
 where sal.order_id is null



-- ============================================================
--  Question 6
--  Show all stores along with any orders placed at each store.
--  Display store_name, store_id (from stores), order_id,
--  and order_date.
--  Every store must appear in the result, even if it has
--  no orders yet.
--  Use sales.orders and sales.stores.
-- ============================================================

-- Write your query below:
select sto.store_name,sto.store_id,ord.order_id,ord.order_date from sales.orders ord
inner join sales.stores sto
on ord.store_id=sto.store_id order by sto.store_id



-- ============================================================
--  Question 7
--  List every staff member alongside their manager's name.
--  Display:
--    • staff full name   (as staff_name)
--    • manager full name (as manager_name)
--  Use only the sales.staffs table.
--  Staff who have no manager should NOT appear in the result.
-- ============================================================

-- Write your query below:
select s.first_name+' '+s.last_name as 'staff_name', m.first_name+' '+m.last_name as 'manager_name' from sales.staffs s
join sales.staffs m
on s.staff_id = m.manager_id




-- ============================================================
--  Question 8
--  Generate every possible combination of store name and
--  brand name.
--  Display store_name and brand_name.
--  Use sales.stores and production.brands.
--  How many total rows do you expect?
--  Write the expected count as a comment next to your query.
-- ============================================================

-- Write your query below:
select sto.store_name,bra.brand_name from sales.stores sto
cross join production.brands bra
---27 rows



-- ============================================================
--  Question 9
--  Retrieve the customer full name (as full_name), order_id,
--  order_date, product_name, and list_price for every order
--  that has been placed.
--  Use sales.customers, sales.orders, sales.order_items,
--  and production.products.
--  Sort by order_date ascending, then full_name ascending.
-- ============================================================

-- Write your query below:
select cus.first_name+' '+cus.last_name as 'full_name',ord.order_id,ord.order_date,pro.product_name,itm.list_price from sales.customers cus
inner join sales.orders ord
on cus.customer_id=ord.customer_id
inner join sales.order_items itm
on ord.order_id=itm.order_id
inner join production.products pro
on itm.product_id=pro.product_id
order by ord.order_date,full_name
