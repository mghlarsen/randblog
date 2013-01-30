class Domain
  include Mongoid::Document
  field :name, type: String
  field :ignore_regexes, type: Array
  has_many :links
end
