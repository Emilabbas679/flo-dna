"use strict";
// Class definition

var KTDatatableHtmlTableDemo = function() {
	// Private functions

	// demo initializer
	var demo = function() {

		var datatable = $('.kt-datatable').KTDatatable({
			data: {
				saveState: {cookie: false},
			},
			search: {
				input: $('#generalSearch'),
			},
			columns: [
				{
					field: 'DepositPaid',
					type: 'number',
				},
				{
					field: 'OrderDate',
					type: 'date',
					format: 'YYYY-MM-DD',
				}, {
					field: 'Status',
					title: 'Status',
					autoHide: false,
					// callback function support for column rendering
					template: function(row) {
						var status = {
							// 1: {'title': 'Pending', 'class': 'kt-badge--brand'},
							// 2: {'title': 'Delivered', 'class': ' kt-badge--danger'},
							// 3: {'title': 'Active', 'class': ' kt-badge--primary'},
							1: {'title': 'Active', 'class': ' kt-badge--success'},
							// 5: {'title': 'Info', 'class': ' kt-badge--info'},
							2: {'title': 'Inactive', 'class': ' kt-badge--danger'},
							// 7: {'title': 'active', 'class': ' kt-badge--warning'},
						};
						let myclass = '';
						if (row.Status=='active'){
							myclass='kt-badge--success';
						}
						else {
							myclass='kt-badge--danger';
						}
						return '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+row.Status+'</span>';
					},
				}, {
					field: 'Type',
					title: 'Type',
					autoHide: false,
					// callback function support for column rendering
					template: function(row) {
						var status = {
							1: {'title': 'Online', 'state': 'danger'},
							2: {'title': 'Retail', 'state': 'primary'},
							3: {'title': 'Direct', 'state': 'success'},
						};
						return '<span class="kt-badge kt-badge--' + status[row.Type].state + ' kt-badge--dot"></span>&nbsp;<span class="kt-font-bold kt-font-' +status[row.Type].state + '">' +	status[row.Type].title + '</span>';
					},
				},
			],
		});

    $('#kt_form_status').on('change', function() {
      datatable.search($(this).val().toLowerCase(), 'Status');
    });

    $('#kt_form_type').on('change', function() {
      datatable.search($(this).val().toLowerCase(), 'Type');
    });

    $('#kt_form_status,#kt_form_type').selectpicker();

	};

	return {
		// Public functions
		init: function() {
			// init dmeo
			demo();
		},
	};
}();

jQuery(document).ready(function() {
	KTDatatableHtmlTableDemo.init();
});