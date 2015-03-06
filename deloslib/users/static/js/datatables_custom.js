/* Set the defaults for DataTables initialisation */
$.extend( true, $.fn.dataTable.defaults, {
    'oLanguage': {
        'oPaginate': {
            'sFirst':    '<i class="fa fa-fast-backward"></i>',
            'sLast':     '<i class="fa fa-fast-forward"></i>',
            'sNext':     '<i class="fa fa-forward"></i>',
            'sPrevious': '<i class="fa fa-backward"></i>'
        },
        'sEmptyTable': 'Sem dados',
        'sInfo': 'Registros _START_ a _END_ de _TOTAL_',
        'sInfoEmpty': 'Sem dados',
        'sInfoFiltered': '(filtrados de _MAX_)',
        'sInfoThousands': '.',
        'sLengthMenu': '_MENU_ por página',
        'sSearch': '<i class="fa fa-filter"></i>',
        'sZeroRecords': 'Sem dados',
        'sProcessing': 'Carregando...',
        'sLoadingRecords': '<i class="fa fa-spinner fa-spin"></i> Carregando...',
    },
    'sPaginationType': 'full_numbers',
    
    'fnServerData': function(source, oaData, callback, settings) {
        settings.jqXHR = $.get(
                source,
                function(data){
                        // Magic happens here! tastypie provides the data but
                        // stupid dataTables requires it to have stupid names 
                        data.echo = oaData.echo;
                        data.iTotalRecords = data.meta.total_count;
                        data.iTotalisplayRecords = data.meta.limit;
                        callback(data);
                        //fnCreateFilterSelect(table, 5);
                }, 
                'json')
        },
} );

/* API method to get paging information */
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
	return {
		"iStart":         oSettings._iDisplayStart,
		"iEnd":           oSettings.fnDisplayEnd(),
		"iLength":        oSettings._iDisplayLength,
		"iTotal":         oSettings.fnRecordsTotal(),
		"iFilteredTotal": oSettings.fnRecordsDisplay(),
		"iPage":          Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
		"iTotalPages":    Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
	};
};


(function($) {
/*
 * Function: fnGetColumnData
 * Purpose:  Return an array of table values from a particular column.
 * Returns:  array string: 1d data array 
 * Inputs:   object:oSettings - dataTable settings object. This is always the last argument past to the function
 *           int:iColumn - the id of the column to extract the data from
 *           bool:bUnique - optional - if set to false duplicated values are not filtered out
 *           bool:bFiltered - optional - if set to false all the table data is used (not only the filtered)
 *           bool:bIgnoreEmpty - optional - if set to false empty values are not filtered from the result array
 * Author:   Benedikt Forchhammer <b.forchhammer /AT\ mind2.de>
 */
$.fn.dataTableExt.oApi.fnGetColumnData = function ( oSettings, iColumn, bUnique, bFiltered, bIgnoreEmpty ) {
	// check that we have a column id
	if ( typeof iColumn == "undefined" ) return new Array();
	
	// by default we only wany unique data
	if ( typeof bUnique == "undefined" ) bUnique = true;
	
	// by default we do want to only look at filtered data
	if ( typeof bFiltered == "undefined" ) bFiltered = true;
	
	// by default we do not wany to include empty values
	if ( typeof bIgnoreEmpty == "undefined" ) bIgnoreEmpty = true;
	
	// list of rows which we're going to loop through
	var aiRows;
	
	// use only filtered rows
	if (bFiltered == true) aiRows = oSettings.aiDisplay; 
	// use all rows
	else aiRows = oSettings.aiDisplayMaster; // all row numbers

	// set up data array	
	var asResultData = new Array();
	
	for (var i=0,c=aiRows.length; i<c; i++) {
		iRow = aiRows[i];
		var aData = this.fnGetData(iRow);
		var sValue = aData[iColumn];
		
		// ignore empty values?
		if (bIgnoreEmpty == true && sValue.length == 0) continue;

		// ignore unique values?
		else if (bUnique == true && jQuery.inArray(sValue, asResultData) > -1) continue;
		
		// else push the value onto the result data array
		else asResultData.push(sValue);
	}
	
	return asResultData;
}}(jQuery));


// Reload current page
$.fn.dataTableExt.oApi.fnReloadAjax = function ( oSettings, sNewSource, fnCallback, bStandingRedraw )
    {
        if ( typeof sNewSource != 'undefined' && sNewSource != null )
    {
        oSettings.sAjaxSource = sNewSource;
    }
    this.oApi._fnProcessingDisplay( oSettings, true );
    var that = this;
    var iStart = oSettings._iDisplayStart;
    var aData = [];

    this.oApi._fnServerParams( oSettings, aData );

    oSettings.fnServerData( oSettings.sAjaxSource, aData, function(json) {
        /* Clear the old information from the table */
        that.oApi._fnClearTable( oSettings );

        /* Got the data - add it to the table */
        var aData =  (oSettings.sAjaxDataProp !== "") ?
            that.oApi._fnGetObjectDataFn( oSettings.sAjaxDataProp )( json ) : json;

        for ( var i=0 ; i<aData.length ; i++ )
        {
            that.oApi._fnAddData( oSettings, aData[i] );
        }

        oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
        that.fnDraw();

        if ( typeof bStandingRedraw != 'undefined' && bStandingRedraw === true )
        {
            oSettings._iDisplayStart = iStart;
            that.fnDraw( false );
        }

        that.oApi._fnProcessingDisplay( oSettings, false );

        /* Callback user function - for event handlers etc */
        if ( typeof fnCallback == 'function' && fnCallback != null )
        {
            fnCallback( oSettings );
        }
    }, oSettings );
}	


function fnCreateFilterSelect( table, column ){
	var aData = table.fnGetColumnData(column);
	
	var r='<select><option value=""></option>', i, iLen=aData.length;
	for ( i=0 ; i<iLen ; i++ )
	{
		r += '<option value="'+aData[i]+'">'+aData[i]+'</option>';
	}
	
	var select = $('<div class="dataTables_filter"></div>').appendTo('.dataTables_wrapper .filters-bar');
	select.html( r+'</select>' );
	$('select', select).change( function () {
		table.fnFilter( $(this).val(), column );
	} );	
}
