{% macro if_null(column) %}
  
    case
        when {{column}} is null then 'not specified'

        else {{column}}
    end 

{%endmacro%}

{% macro if_null_zero(column, type_hint= 'DOUBLE') %}

    cast(case 
        when {{column}} is null THEN 0.0
        else {{column}}
    end AS {{type_hint}})

{% endmacro %}