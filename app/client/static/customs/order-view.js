"use strict";
var KTDatatablesBasicScrollable = function() {

	var initTable1 = function() {
		var table = $('#kt_table_1');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable2 = function() {
		var table = $('#kt_table_2');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable3 = function() {
		var table = $('#kt_table_3');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable4 = function() {
		var table = $('#kt_table_4');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable5 = function() {
		var table = $('#kt_table_5');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable6 = function() {
		var table = $('#kt_table_6');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable7 = function() {
		var table = $('#kt_table_7');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable8 = function() {
		var table = $('#kt_table_8');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable9 = function() {
		var table = $('#kt_table_9');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable10 = function() {
		var table = $('#kt_table_10');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	var initTable11 = function() {
		var table = $('#kt_table_11');
		table.DataTable({
			scrollY: '50vh',
			scrollX: true,
			scrollCollapse: true,
			createdRow: function(row, data, index) {
				status =row.getElementsByTagName('td')[1].textContent
				let myclass = '';
				if (status=='pending'){
					myclass='kt-badge--brand';
				}
				else if(status == 'rejected'){
					myclass='kt-badge--danger';
				}
				else if(status == 'done'){
					myclass='kt-badge--primary';
				}
				else if(status == 'accepted'){
					myclass='kt-badge--success';
				}
				else {
					myclass='kt-badge--info';
				}
				var badge = '<span class="kt-badge '+myclass+' kt-badge--inline kt-badge--pill">'+status+'</span>';
				row.getElementsByTagName('td')[1].innerHTML = badge;
			},
		});
	};
	return {

		//main function to initiate the module
		init: function() {
			initTable1();
			initTable2();
			initTable3();
			initTable4();
			initTable5();
			initTable6();
			initTable7();
			initTable8();
			initTable9();
			initTable11();
			initTable10();
		},

	};

}();

jQuery(document).ready(function() {
	KTDatatablesBasicScrollable.init();
});