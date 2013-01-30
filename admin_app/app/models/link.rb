class Link
  include Mongoid::Document
  field :url, type: String
  field :sources, type: Array
  belongs_to :domain

  def srcs
    sources.map {|source| CorpusItem.find(source)}
  end
end
