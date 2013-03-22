module ApplicationHelper
  def info_row(name, value)
    render partial: 'shared/info_row', locals: {name: name, value: value}
  end

  def info_table_hash(info)
    render partial: 'shared/info_table_hash', locals: {info: info}
  end

  def info_table_hash_list(list)
    render partial: 'shared/info_table_list', locals: {list: list}
  end

  def info_form_row(name, field, type, form)
    render partial: 'shared/info_form_row', locals: {name: name, field: field, type: type, form: form}
  end
end
