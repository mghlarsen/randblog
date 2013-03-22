class FeedCleanActionsController < ApplicationController
  # GET /feeds/1/clean_actions/1
  def index
    @clean_actions = Feed.find(params[:feed_id]).feed_clean_actions
  end

  def show
  end

  def new
  end

  def edit
  end

  def create
  end

  def update
  end

  def destroy
  end
end
