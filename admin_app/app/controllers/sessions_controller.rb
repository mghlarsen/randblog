class SessionsController < ApplicationController
  def create
    auth = request.env['omniauth.auth']
    if User.where(provider: auth['provider'], uid: auth['uid']).exists?
      puts "User Exists!"
      puts auth
      user = User.where(provider: auth['provider'], uid: auth['uid']).first 
      user.update_info(auth)
      user.save!
    else
      puts "New User"
      user = User.create_with_omniauth(auth)
    end
    session[:user_id] = user.id
    redirect_to root_url, notice: 'Signed in!'
  end

  def destroy
    reset_session
    redirect_to root_url, notice: 'Signed out!'
  end

  def new
    redirect_to '/auth/google_oauth2'
  end

  def failure
    redirect_to root_url, alert: "Authentication error: #{params[:message].humanize}"
  end

  def info
    authenticate_user!
  end
end
