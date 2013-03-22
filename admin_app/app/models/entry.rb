require 'nokogiri'

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

  def body
    if attributes.include? 'content' && content.length > 0
      content
    else
      summary
    end
  end

  def cleaned_doc
    if !@doc
      if attributes.include? 'content' && content.length > 0
        @html = content
      else
        @html = summary
      end
      @doc = Nokogiri::HTML(@html)
      feed.clean_doc(@doc)
    end
    @doc
  end

  def cleaned_text
    cleaned_doc.inner_text
  end

  def cleaned_html
    cleaned_doc.inner_html
  end
end
