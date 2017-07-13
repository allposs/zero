$(function () {
 	var url = '';
    var datagrid; //定义全局变量datagrid
    var editRow = undefined; //定义全局变量：当前编辑的行
    datagrid = $("#dd").datagrid({
        url: '/api/listapi', //请求的数据源
		queryParams: { 
			name: 'easyui',         
			subject: 'datagrid'     
			},
        iconCls: 'icon-save', //图标
        pagination: true, //显示分页
        pageSize: 15, //页大小
        pageList: [15, 30, 45, 60], //页大小下拉选项此项各value是pageSize的倍数
        fit: false, //datagrid自适应宽度
        fitColumn: true, //列自适应宽度
        striped: true, 										//行背景交换
        nowap: true, 										//列内容多时自动折至第二行
        border: false,
        idField: 'UUID', 									//主键
        columns: [[											//显示的列
			{ field: 'UUID', title: '编号', width: 100, sortable: true, checkbox: true },
			{ field: 'Asset_Number', title: '资产编号', width: 100, sortable: true,
				editor: { type: 'validatebox', options: { required: true} }
			},
			{ field: 'Service_Model', title: '服务器型号', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'CPU_Numbers', title: 'CPU数量', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'CPU_Model', title: 'CPU型号', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'Memory_Numbers', title: '内存数量', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'Memory_Model', title: '内存型号', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'Memory_Capacity', title: '内存容量', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'Disk_Numbers', title: '硬盘数量', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'Disks_Model', title: '硬盘类型', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'Disks_Capacity', title: '硬盘容量', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'NetworkCar_Model', title: '网卡型号', width: 100,
				editor: { type: 'validatebox' }
			},
			{ field: 'NetworkCar_Numbers', title: '网卡数量', width: 100,
				editor: { type: 'validatebox'}
			}
        ]],
        queryParams: { action: 'query' }, 											//查询参数
        toolbar: [
			{ text: '添加', iconCls: 'icon-add', handler: function () {				//添加列表的操作按钮添加，修改，删除等            	
				
				if (editRow != undefined) {											//添加时先判断是否有开启编辑的行，如果有则把开户编辑的那行结束编辑
					$.messager.confirm("提示", "你有未保存的编辑，是否保存！", function (r) {
						if (r) {													//提示用户是否保存上次编辑
							datagrid.datagrid("endEdit", editRow);
							url = '/api/updateapi';	
							}
						else {
							datagrid.datagrid("rejectChanges");
							url = '/api/addapi';
							datagrid.datagrid("insertRow", {						
								index: 0, 													// index start with 0
								row: {

								}
							});
							datagrid.datagrid("beginEdit", 0);								//将新插入的那一行开户编辑状态                        
							editRow = 0;													//给当前编辑的行赋值
						}
                    });
                }
					           
				if (editRow == undefined) {											//添加时如果没有正在编辑的行，则在datagrid的第一行插入一行
					url = '/api/addapi';
					datagrid.datagrid("insertRow", {
						
						index: 0, 													// index start with 0
						row: {

						}
					});                       
					datagrid.datagrid("beginEdit", 0);								//将新插入的那一行开户编辑状态                        
					editRow = 0;													//给当前编辑的行赋值
				}

			}}, '-',
			
			{ text: '删除', iconCls: 'icon-remove', handler: function () {                    
                var rows = datagrid.datagrid("getSelections");						//删除时先获取选择行                    
                if (rows.length > 0) {												//选择要删除的行
                    $.messager.confirm("提示", "你确定要删除吗?", function (r) {
                        if (r) {
							var list = [1,2];
                            var ids = [];
                            for (var i = 0; i < rows.length; i++) {					//将选择到的行存入数组并用,分隔转换成字符串，
                                ids.push(rows[i].UUID);
							}
							$.ajax({															//以AJAX数据传输到后台
								type : 'POST',
								url : '/api/delapi',
								data :{
									UUID: ids,
								},
					
								beforeSend: function(){
									datagrid.datagrid('loading');
								},
					
								success: function(data){
									if (data) {
										datagrid.datagrid('loaded');
										datagrid.datagrid('load');
										datagrid.datagrid('unselectAll');
									}
								},

							});
                        }
                    });
                }
				else {
                     $.messager.alert("提示", "请选择要删除的行", "error");
                }
			}}, '-',
			
            { text: '修改', iconCls: 'icon-edit', handler: function () {   
                var rows = datagrid.datagrid("getSelections");						//如果只选择了一行则可以进行修改，否则不操作
				
                if (rows.length == 1) {											//修改之前先关闭已经开启的编辑行，当调用endEdit该方法时会触发onAfterEdit事件
                    if (editRow != undefined) {
                        datagrid.datagrid("endEdit", editRow);
							
							
                    }                         
                    if (editRow == undefined) {									//当无编辑行时   
						url='/api/updateapi';
						var index = datagrid.datagrid("getRowIndex", rows[0]);	//获取到当前选择行的下标                             
						datagrid.datagrid("beginEdit", index);					//开启编辑                            
                        editRow = index;										//把当前开启编辑的行赋值给全局变量editRow
                        datagrid.datagrid("unselectAll");						//当开启了当前选择行的编辑状态之后，应该取消当前列表的所有选择行，要不然双击之后无法再选择其他行进行编辑
                    }
                }
            }}, '-',
			
            { text: '保存', iconCls: 'icon-save', handler: function () {
                    
                datagrid.datagrid("endEdit", editRow);								//保存时结束当前编辑的行，自动触发onAfterEdit事件如果要与后台交互可将数据通过Ajax提交后台
            }}, '-',
                 
			{ text: '取消编辑', iconCls: 'icon-redo', handler: function () {		//取消当前编辑行把当前编辑行罢undefined回滚改变的数据,取消选择的行     
                editRow = undefined;
                datagrid.datagrid("rejectChanges");
                datagrid.datagrid("unselectAll");
            }}, '-'
			],
                
		onAfterEdit: function (rowIndex, rowData, changes) {					//endEdit该方法触发此事件
                    
            console.info(rowData);
            editRow = undefined;
			$.ajax({															//以AJAX数据传输到后台
				type : 'POST',
				url : url,
				data : rowData,
					
				beforeSend: function(){
					datagrid.datagrid('loading');
				},
					
				success: function(data){
					if (data) {
						datagrid.datagrid('loaded');
						datagrid.datagrid('load');
						datagrid.datagrid('unselectAll');
						}
					},
				});
            },
        onDblClickRow: function (rowIndex, rowData) {
					
                    if (editRow != undefined) {
                        datagrid.datagrid("endEdit", editRow);
                    }
                    if (editRow == undefined) {
                        datagrid.datagrid("beginEdit", rowIndex);
                        editRow = rowIndex;
                    }
                }
        });
});
