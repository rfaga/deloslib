/***** adapting backbone-pageable to tastypie */
Backbone.PageableCollection.prototype.parse = function( data ) {
	if ( data && data.meta ) {
		this.meta = data.meta;
	}

	return data && data.objects || data;
};

Backbone.PageableCollection.prototype.url = function( models ) {
	var url = _.isFunction( this.urlRoot ) ? this.urlRoot() : this.urlRoot;
	// If the collection doesn't specify an url, try to obtain one from a model in the collection
	if ( !url ) {
		var model = models && models.length && models[ 0 ];
		url = model && ( _.isFunction( model.urlRoot ) ? model.urlRoot() : model.urlRoot );
	}
	url = url && addSlash( url );

	// Build a url to retrieve a set of models. This assume the last part of each model's idAttribute
	// (set to 'resource_uri') contains the model's id.
	if ( models && models.length ) {
		var ids = _.map( models, function( model ) {
			var parts = _.compact( model.id.split( '/' ) );
			return parts[ parts.length - 1 ];
		});
		url += 'set/' + ids.join( ';' ) + '/';
	}

	return url || null;
};

Backbone.FilteredPageableCollection = Backbone.PageableCollection.extend({
  	initialize : function(){
  		Backbone.PageableCollection.prototype.initialize.apply(this);
  		this.filtersEnabled = {};
  	},
  	
  	setFilter : function(name, value){
		this.filtersEnabled[name] = value;
		this.processFilters();
	},
	
	processFilters : function() {
		var filtered = [], 
			fullColl = this.fullCollection, 
			allModels = this.fullModels || fullColl.models;
			self = this;
		// Reset the filter to normal
		fullColl.reset(allModels);
		// Keep a copy of *all* the models
		this.fullModels = this.fullModels || fullColl.models.slice(0);
				
		_.each(this.filtersEnabled, function(value, key){
			if (value != ''){
				filtered = self.filter(function(model) {
					return model.get(key) === value;
				});
				fullColl.reset(filtered, {});
			}
		});
	}
});


/***** Changing default backbone-forms *****/
Backbone.Form.editors.TimeDatePicker = Backbone.Form.editors.Text.extend({
    render: function() {
        // Call the parent's render method
        Backbone.Form.editors.Text.prototype.render.call(this);
        // Then make the editor's element a datepicker.
        this.$el.datetimepicker({
            format: 'dd/mm/yyyy hh:mm',
            autoclose: true,
            weekStart: 1
        });

        return this;
    },
    // The set value must correctl
    setValue: function(value) {
        try{
        	this.$el.val(moment(value).format('YYYY-MM-DD HH:MM'));
        } catch (err){
       		this.$el.val(moment().format('YYYY-MM-DD HH:MM'));
        }
    }
});

Backbone.Form.editors.DatePicker = Backbone.Form.editors.Text.extend({
    render: function() {
        // Call the parent's render method
        Backbone.Form.editors.Text.prototype.render.call(this);
        // Then make the editor's element a datepicker.
        this.$el.datepicker({
            format: 'dd/mm/yyyy',
            autoclose: true,
            weekStart: 1
        });

        return this;
    },

    // The set value must correctl
    setValue: function(value) {
    	try{
        	this.$el.val(moment(value).format('DD/MM/YYYY'));
        } catch (err){
       		this.$el.val(moment().format('DD/MM/YYYY'));
        }
    }
});

Backgrid.ActionsCell = Backgrid.Cell.extend({
  template: _.template("<a class='btn remove btn-danger' title='Remove'><i class='icon-trash'></i></a>"),
    events: {
      "click a.remove": "confirmRemoveRow"
    },
    confirmRemoveRow : function(event){
        var self = this;
        bootbox.confirm("Tem certeza que deseja remover este registro?", function(result){
            if (result){
                self.removeRow(event);
            }
        });
    },
    removeRow: function(event) {
        var self = this;
        temp=this.model;
        self.model.url = self.model.get('resource_uri');
        self.model.destroy({success: function(model, response){
            var currentRow = $(event.currentTarget).parents('tr');
            currentRow.hide('slow', function(){ currentRow.remove(); });
        }});
    },
    render: function () {
      this.$el.html(this.template());
      this.delegateEvents();
      return this;
    }
});

Backbone.CrudView = Backbone.View.extend({
	render : function(){
		var self = this;
		this.collection = new this.CollectionClass();
		this.collection.fetch({
			success : function(collection) {
				self.renderCollection();
			},
			reset: true
		});
	},
	events : {
		'click a.new-item': "newItem",
	},
	newItem : function(event){
		event.preventDefault();
		this.collection.create();
	},
	renderCollection : function(){
		var self = this;
		// Initialize a new Grid instance
		this.grid = new Backgrid.Grid({
		  columns: self.columns,
		  collection: this.collection
		});
		this.grid.listenTo(this.collection,"backgrid:edited",function(e){
			e.url = e.base_url();
			e.save();
		});
		
		var filter = new Backgrid.Extension.ClientSideFilter({
		  collection: self.collection.fullCollection,
		  fields: self.filterFields
		});
		this.$el.append(filter.render().$el);
		
		var template = _.template($("#list_template").html());
		this.$el.append(this.grid.render().$el);
		this.$el.append(template);
		
		var paginator = new Backgrid.Extension.Paginator({
		  collection: self.collection
		});
		this.$el.append(paginator.render().$el);
		
	}
});

Backbone.DelosModel = Backbone.Model.extend({
	base_url: function() {
	    var temp_url = Backbone.Model.prototype.url.call(this);
	    return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/');
    },
    str : function(){
    	return this.title;
    },
});

Number.prototype.formatMoney = function(c, d, t){
var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c, 
    d = d == undefined ? "," : d, 
    t = t == undefined ? "." : t, 
    s = n < 0 ? "-" : "", 
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
    j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };