class Output
  include Mongoid::Document
  store_in collection: 'output'
  field :date, type: DateTime
  field :text, type: String
  field :type, type: String
  field :nGram, type: Integer
end
