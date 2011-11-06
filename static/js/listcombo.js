/*
Mootools-based list-based combobox
Ray Gregory.
Inspired by and derived from comboboo.js (Bruno Torrinha - www.torrinha.com).
*/

var ListCombo = new Class({
    
    Implements: [Options],
    
    options: {class_name: 'ListCombo'},
    
    initialize: function(ulist, select_event, norm_bg, hl_bg, options)
    {
        this.setOptions(options);
        this.IsOpen = false;
        this.NormalBGColor = norm_bg;
        this.HilightBGColor = hl_bg;
        this.SelectEventHandler = select_event;
        
        var sel_elements = ulist.getElements('li.ListComboSelected');
        
        var selected_text = sel_elements[0].get('html');
        
        var list_elements = ulist.getElements('li');
        
        list_elements[list_elements.length-1].setStyle('border-bottom-left-radius','6px');
        list_elements[list_elements.length-1].setStyle('border-bottom-right-radius','6px'); 
        
        this.list_combo_link = new Element('a', {'class': this.options.class_name + 'Label', 'id': ''}).set('html', selected_text);
        ulist.parentNode.insertBefore( this.list_combo_link, ulist);
        this.list_combo_list = ulist;
        
        this.list_combo_list.set('tween',
        {
            onComplete: function()
            {
                if (this.IsOpen)
                {
                    this.list_combo_link.setStyle('border-bottom-left-radius','0px');
                    this.list_combo_link.setStyle('border-bottom-right-radius','0px');
                    this.list_combo_list.setStyle('display', 'inherit');
                }
                else
                {
                    this.list_combo_link.setStyle('border-bottom-left-radius','6px');
                    this.list_combo_link.setStyle('border-bottom-right-radius','6px');
                    this.list_combo_list.setStyle('display', 'none');
                }              
            }.bind(this)
        }); 
        
        this.fx={lclink: this.list_combo_link.set('tween','background-color', {duration:150}).tween('background-color',this.NormalBGColor),
            lclist: this.list_combo_list.set('tween','opacity',{duration:150}).tween('opacity',0)};
        
        this.RegisterComboLinkEvents(this.list_combo_link);
        
        for(i=0; i< list_elements.length; ++i)
        {
            this.RegisterComboChoiceEvents(list_elements[i]);                
        }
        
        this.list_combo_list.setStyle('display','');
    },
    
    ComboOver: function()
    {
        if (!this.IsOpen)
        {
            this.fx.lclink.tween('background-color',this.HilightBGColor);
        }
    },
    
    ComboOut: function(combo_element)
    {
        if (!this.IsOpen)
        {
            this.fx.lclink.tween('background-color',this.NormalBGColor);
        }
    },
    
    ComboClick: function(combo_element)
    {
        if (this.IsOpen)
        {
            this.IsOpen = false;
            this.list_combo_link.removeClass('combo-open');
            this.list_combo_link.addClass('combo-closed');
            this.fx.lclist.tween('opacity','0');
            //this.list_combo_link.setStyle('border-bottom-left-radius','6px');
            //this.list_combo_link.setStyle('border-bottom-right-radius','6px');  
        }
        else
        {
            this.IsOpen = true;
            this.list_combo_link.removeClass('combo-closed');
            this.list_combo_link.addClass('combo-open');
            this.list_combo_link.setStyle('border-bottom-left-radius','0px');
            this.list_combo_link.setStyle('border-bottom-right-radius','0px');
            this.list_combo_list.setStyle('display', 'inherit');
            this.fx.lclist.tween('opacity','1');
        }
    },
    
    ChoiceOver: function(choice_element)
    {
        if (this.selected)
        {
            this.selected.removeClass('choice-selected');
        }
        this.selected = choice_element.addClass('choice-selected');
    },
    
    ChoiceSelect: function(choice_element)
    {
        this.IsOpen = false;
        this.fx.lclink.tween('background-color',this.NormalBGColor);
        this.fx.lclist.tween('opacity','0');
        var selection_text =  choice_element.get('text');
        this.list_combo_link.set('html', selection_text);
        this.SelectEventHandler(selection_text);
    },
    
    RegisterComboLinkEvents: function(link_element)
    {
        return link_element.addEvents({
            click: this.ComboClick.bind(this, [link_element]),
            mouseover: this.ComboOver.bind(this, [link_element]),
            mouseleave: this.ComboOut.bind(this, [link_element])});
    },

    RegisterComboChoiceEvents: function(choice_element)
    {
        return choice_element.addEvents({
            mouseover: this.ChoiceOver.bind(this, [choice_element]),
            mousedown: this.ChoiceSelect.bind(this, [choice_element])});
    }
    
});

ListCombo.implement(new Events, new Options);






