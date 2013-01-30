class LinkFilter
  include Mongoid::Document
  field :name_regex, type: String
end
