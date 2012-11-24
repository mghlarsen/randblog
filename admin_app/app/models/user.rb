class User
  include Mongoid::Document
  field :provider, type: String
  field :uid, type: String
  field :name, type: String
  field :email, type: String
  field :info, type: Hash
  field :extra, type: Hash
  field :credentials, type: Hash

  attr_protected :provider, :uid, :name, :email

  def self.create_with_omniauth(auth)
    create! do |user|
      user.provider = auth['provider']
      user.uid = auth['uid']
      if auth['info']
        user.name = auth['info']['name'] || ''
        user.email = auth['info']['email'] || ''
      end
      user.info = auth['info'] || nil
      user.extra = auth['extra'] || nil
      user.credentials = auth['credentials'] || nil
    end
  end

  def update_info(auth)
    if auth['info']
      update_attributes(
        name: auth['info']['name'] || '',
        email: auth['info']['email'] || ''
      )
    end
    update_attributes(
        info: auth['info'] || nil,
        extra: auth['extra'] || nil,
        credentials: auth['credentials'] || nil
    )
  end
end
