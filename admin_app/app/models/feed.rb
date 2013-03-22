class Feed
  include Mongoid::Document
  field :name, type: String
  field :title, type: String
  field :subtitle, type: String
  field :url, type: String
  field :link, type: String
  field :status, type: Hash

  has_many :entries, foreign_key: :feed
  embeds_many :feed_clean_actions, store_as: :clean_actions

  def clean_doc(doc)
    feed_clean_actions.each{|action| action.perform(doc)}
  end

  store_in collection: 'feed'
end
