class CorpusItem
  include Mongoid::Document
  store_in collection: 'items'
  field :text, type: String
  field :source, type: Hash
  field :published, type: DateTime
  field :updated, type: DateTime
  field :links, type: Array

  def filter_attributes(excluded_fields)
    attributes.reject do |key, value|
      excluded_fields.include?(key)
    end
  end
end
