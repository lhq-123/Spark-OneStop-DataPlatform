-- 油站数量
-- 新增油站数量
-- 维度
--     日期维度(月)
--     日期维度(周)
--     日期维度(日)
--     油站维度(油站类型)
--     油站维度(油站所属省)
--     油站维度(油站所属市)
--     油站维度(油站所属区)
--     客户维度(客户类型)
--     客户维度(客户所属省)
select
    sum(oil.os_num) sum_osnum, sum(oil.current_new_os_num) sumnew_osnum,
    dd.date_id dws_day, dd.week_in_year_id dws_week, dd.year_month_id dws_month, dimoil.company_name oil_type, dimoil.province_name oil_province,
    dimoil.city_name oil_city, dimoil.county_name oil_county, dimoil.customer_classify_name customer_classify, dimoil.customer_province_name customer_province
from one_make_dwb.fact_oil_station oil
         left join one_make_dws.dim_date dd on oil.dt = dd.date_id
         left join one_make_dws.dim_oilstation dimoil on oil.os_id = dimoil.id
group by dd.date_id, dd.week_in_year_id, dd.year_month_id,  dimoil.company_name, dimoil.province_name, dimoil.city_name, dimoil.county_name,
         dimoil.customer_classify_name, dimoil.customer_province_name
;

-- 装载数据
insert overwrite table one_make_st.subj_oilstation partition(month = '202101', week='2021W1', day='20210101')
select
    sum(oil.os_num) sum_osnum, sum(oil.current_new_os_num) sumnew_osnum,
    dd.date_id dws_day, dd.week_in_year_id dws_week, dd.year_month_id dws_month, dimoil.company_name oil_type, dimoil.province_name oil_province,
    dimoil.city_name oil_city, dimoil.county_name oil_county, dimoil.customer_classify_name customer_classify, dimoil.customer_province_name customer_province
from one_make_dwb.fact_oil_station oil
    left join one_make_dws.dim_date dd on oil.dt = dd.date_id
    left join one_make_dws.dim_oilstation dimoil on oil.os_id = dimoil.id
where dd.year_month_id = '202101'and dd.week_in_year_id = '2021W1' and  dd.date_id = '20210101'
group by dd.date_id, dd.week_in_year_id, dd.year_month_id,  dimoil.company_name, dimoil.province_name, dimoil.city_name, dimoil.county_name,
    dimoil.customer_classify_name, dimoil.customer_province_name
;