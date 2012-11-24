class Entry
  include Mongoid::Document
  store_in collection: 'entries'
  field :feed_name, type: String
  field :links, type: Array
  field :id, type: String

  belongs_to :feed, foreign_key: :feed
end
