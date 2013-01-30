class LinkFiltersController < ApplicationController
  # GET /link_filters
  # GET /link_filters.json
  def index
    @link_filters = LinkFilter.all

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @link_filters }
    end
  end

  # GET /link_filters/1
  # GET /link_filters/1.json
  def show
    @link_filter = LinkFilter.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @link_filter }
    end
  end

  # GET /link_filters/new
  # GET /link_filters/new.json
  def new
    @link_filter = LinkFilter.new

    respond_to do |format|
      format.html # new.html.erb
      format.json { render json: @link_filter }
    end
  end

  # GET /link_filters/1/edit
  def edit
    @link_filter = LinkFilter.find(params[:id])
  end

  # POST /link_filters
  # POST /link_filters.json
  def create
    @link_filter = LinkFilter.new(params[:link_filter])

    respond_to do |format|
      if @link_filter.save
        format.html { redirect_to @link_filter, notice: 'Link filter was successfully created.' }
        format.json { render json: @link_filter, status: :created, location: @link_filter }
      else
        format.html { render action: "new" }
        format.json { render json: @link_filter.errors, status: :unprocessable_entity }
      end
    end
  end

  # PUT /link_filters/1
  # PUT /link_filters/1.json
  def update
    @link_filter = LinkFilter.find(params[:id])

    respond_to do |format|
      if @link_filter.update_attributes(params[:link_filter])
        format.html { redirect_to @link_filter, notice: 'Link filter was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: "edit" }
        format.json { render json: @link_filter.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /link_filters/1
  # DELETE /link_filters/1.json
  def destroy
    @link_filter = LinkFilter.find(params[:id])
    @link_filter.destroy

    respond_to do |format|
      format.html { redirect_to link_filters_url }
      format.json { head :no_content }
    end
  end
end
