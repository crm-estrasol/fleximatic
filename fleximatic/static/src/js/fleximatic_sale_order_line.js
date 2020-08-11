
odoo.define('tomcat.tomcat_sale_order_line', function (require) {
   
            
            "use strict";
        
            var SectionAndNoteListRenderer = require('account.section_and_note_backend');
        
            var  a = SectionAndNoteListRenderer
        
            SectionAndNoteListRenderer.include({
                /**
             * We want section and note to take the whole line (except handle and trash)
             * to look better and to hide the unnecessary fields.
             *
             * @override
             */
            _renderBodyCell: function (record, node, index, options) {
                var $cell = this._super.apply(this, arguments);
                var isPromotional = record.data.is_promotional === true;
               
                if(isPromotional){
                    if (node.attrs.widget === "handle") {
                        return $cell;
                    } else if (node.attrs.name === "name" ||  node.attrs.name === "product_id" ||  node.attrs.name === "product_uom_qty" |  node.attrs.name === "price_subtotal") {
                        
                        
                    } else {
                        $cell.removeClass('o_invisible_modifier');
                        return $cell.addClass('o_hidden');
                    }   

                }
               

                return $cell;
            },
            /**
             * We add the o_is_{display_type} class to allow custom behaviour both in JS and CSS.
             *
             * @override
             */
            _renderRow: function (record, index) {
                var $row = this._super.apply(this, arguments);

                if (record.data.is_promotional) {
                   //$row.find('.o_list_record_remove').addClass('o_hidden');
                   $row.find('.o_list_record_remove').remove();
                   return  $row
                }
                
                
                return $row;
            },
        
    });
    
   
    });
    