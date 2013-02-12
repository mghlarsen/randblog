class CorpusItemsController < ApplicationController
  # GET /corpus_items
  # GET /corpus_items.json
  def index
    @corpus_items = CorpusItem.all.desc(:published).limit(params[:limit] || 100)

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @corpus_items }
    end
  end

  # GET /corpus_items/1
  # GET /corpus_items/1.json
  def show
    @corpus_item = CorpusItem.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @corpus_item }
    end
  end

  # GET /corpus_items/new
  # GET /corpus_items/new.json
  def new
    @corpus_item = CorpusItem.new

    respond_to do |format|
      format.html # new.html.erb
      format.json { render json: @corpus_item }
    end
  end

  # GET /corpus_items/1/edit
  def edit
    @corpus_item = CorpusItem.find(params[:id])
  end

  # POST /corpus_items
  # POST /corpus_items.json
  def create
    @corpus_item = CorpusItem.new(params[:entry])

    respond_to do |format|
      if @corpus_item.save
        format.html { redirect_to @corpus_item, notice: 'CorpusItem was successfully created.' }
        format.json { render json: @corpus_item, status: :created, location: @corpus_item }
      else
        format.html { render action: "new" }
        format.json { render json: @corpus_item.errors, status: :unprocessable_entity }
      end
    end
  end

  # PUT /corpus_items/1
  # PUT /corpus_items/1.json
  def update
    @corpus_item = CorpusItem.find(params[:id])

    respond_to do |format|
      if @corpus_item.update_attributes(params[:entry])
        format.html { redirect_to @corpus_item, notice: 'CorpusItem was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: "edit" }
        format.json { render json: @corpus_item.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /corpus_items/1
  # DELETE /corpus_items/1.json
  def destroy
    @corpus_item = CorpusItem.find(params[:id])
    @corpus_item.destroy

    respond_to do |format|
      format.html { redirect_to corpus_items_url }
      format.json { head :no_content }
    end
  end
end
