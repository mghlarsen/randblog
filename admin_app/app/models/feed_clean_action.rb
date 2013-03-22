class FeedCleanAction
  include Mongoid::Document
  embedded_in :feed

  field :selector, type: String 
  field :task, type: String
  field :contains_text, type: String
  field :match_text, type: String

  def perform(doc)
    doc.css(selector).each do |node|
      pass = true
      if attributes.include? 'match_text'
        pass &&= node.inner_text.strip == match_text
      end
      if attributes.include? 'contains_text'
        pass &&= node.inner_text.include? contains_text
      end
      if pass
        if task == 'remove'
          node.remove
        end
      end 
    end
  end
end

