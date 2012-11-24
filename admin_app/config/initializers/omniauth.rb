ENV['GOOGLE_KEY'] = '583005232653.apps.googleusercontent.com'
ENV['GOOGLE_SECRET'] = '9DQvL1cdniHIp-vE8jZnlI6W'

Rails.application.config.middleware.use OmniAuth::Builder do
  provider :google_oauth2, ENV['GOOGLE_KEY'], ENV['GOOGLE_SECRET'], {
    access_type: 'offline',
    approval_prompt: '',
    scope: 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/blogger',
    client_options: {ssl: {ca_path: '/etc/pki/tls/certs'}}
  } 
end

