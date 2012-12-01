class Entry
  include Mongoid::Document
  store_in collection: 'entries'
  field :feed_name, type: String
  field :links, type: Array
  field :id, type: String
  field :author, type: String

  belongs_to :feed, foreign_key: :feed
  belongs_to :corpus_item, foreign_key: :corpus_item

  def filter_attributes(excluded_fields)
    attributes.reject do |key, value|
      excluded_fields.include?(key)
    end
  end
end
