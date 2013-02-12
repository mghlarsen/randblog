class CorpusItem
  include Mongoid::Document
  store_in collection: 'corpus_item'
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

  def source_obj
    begin
      if source['type'] == 'rss'
        @source_obj = Entry.find(source['entry'])
      elsif source['type'] == 'link'
        @source_obj = Link.find(source['link'])
      end
    rescue Mongoid::Errors::DocumentNotFound
      @source_obj = nil
    end
  end
end
