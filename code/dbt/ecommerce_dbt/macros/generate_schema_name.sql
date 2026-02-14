{% macro generate_schema_name(custom_schema_name, node) -%}
  {# 
    dbt por defecto concatena: target.schema + '_' + custom_schema_name
    Con este macro lo hacemos "enterprise-clean":
    - si el modelo define +schema: STAGING => escribe en STAGING
    - si define +schema: MARTS   => escribe en MARTS
    - si no define schema, usa target.schema (por ejemplo DBT)
  #}
  {%- if custom_schema_name is none -%}
    {{ target.schema }}
  {%- else -%}
    {{ custom_schema_name | trim }}
  {%- endif -%}
{%- endmacro %}
