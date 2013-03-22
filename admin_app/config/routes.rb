AdminApp::Application.routes.draw do
  resources :link_filters
  resources :domains
  resources :links
  resources :outputs
  resources :corpus_items
  resources :entries
  resources :feeds do
    resources :clean_actions, controller: 'feed_clean_actions'
  end

  root to: 'home#index'

  match '/auth/info' => 'sessions#info'
  match '/auth/:provider/callback' => 'sessions#create'
  match '/auth/failure' => 'sessions#failure'
  match '/signout' => 'sessions#destroy', :as => :signout
  match '/signin' => 'sessions#new', :as => :signin
end
