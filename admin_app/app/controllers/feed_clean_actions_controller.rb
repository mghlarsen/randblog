class FeedCleanActionsController < ApplicationController
  before_filter :load_feed
  before_filter :load_action, only: [:show, :edit, :update, :destroy]

  # GET /feeds/1/clean_actions
  def index
  end

  # GET /feeds/1/clean_actions/1
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
    @clean_action.destroy

    respond_to do |format|
      format.html { redirect_to feed_clean_actions(@feed) }
      format.json { head :no_content }
    end
  end

  private
  def load_feed
    @feed = Feed.find(params[:feed_id])
    @clean_actions = @feed.feed_clean_actions
  end

  def load_action
    @clean_action = @clean_actions.find(params[:id])
  end
end
