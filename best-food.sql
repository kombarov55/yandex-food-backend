with avg_summary as (select avg(price) avg_price, avg(weight) avg_weight, avg(r.rating) avg_rating
                     from food
                              join restaurant r on food.restaurant_id = r.slug
                     where food.xlsx_request_id = 1
                       and food.place_type = :place_type
                       and (food.name like :name || '%' or food.name like '%' || :name || '%' or
                            food.name like :lower_name || '%' or food.name like '%' || :lower_name || '%')
)
select food.name, food.src, food.price, food.weight, food.restaurant_id, food.external_id, food.category_id, food.id,
       (1 - (cast((food.price - avg_summary.avg_price) as real) / avg_summary.avg_price)) +
       cast((food.weight - avg_summary.avg_weight) as real) / avg_summary.avg_weight +
       cast((r.rating - avg_summary.avg_rating) as real) / avg_summary.avg_rating as percent_sum
from food
         join restaurant r on food.restaurant_id = r.slug join avg_summary on true
where food.xlsx_request_id = 1
  and food.place_type = :place_type
  and (food.name like :name || '%' or food.name like '%' || :name || '%' or food.name like :lower_name || '%' or
       food.name like '%' || :lower_name || '%')
order by percent_sum desc
limit :amount;