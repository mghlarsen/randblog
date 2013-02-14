class Entry
  include Mongoid::Document
  store_in collection: 'entry'
  field :feed_name, type: String
  field :links, type: Array
  field :entry_id, type: String
  field :author, type: String
  field :published, type: DateTime
  field :updated, type: DateTime

  belongs_to :feed, foreign_key: :feed
  belongs_to :corpus_item, foreign_key: :corpus_item
end
