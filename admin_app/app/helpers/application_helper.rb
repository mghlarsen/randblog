module ApplicationHelper
  def info_row(name, value)
    render partial: 'shared/info_row', locals: {name: name, value: value}
  end
end
