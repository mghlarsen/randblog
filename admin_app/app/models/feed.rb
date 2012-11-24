class Feed
  include Mongoid::Document
  field :name, type: String
  field :title, type: String
  field :subtitle, type: String
  field :url, type: String
  field :link, type: String
  field :status, type: Hash

  has_many :entries, foreign_key: :feed
end
