
//appbase: javascript for this web app

function ToggleHeaderInfo()
{    
    var common_duration = 250;
    var common_transition =  Fx.Transitions.linear.easeInOut;
    
    var info_trans = new Fx.Elements([$('hbup'),$('hbbgl'),$('hbbgr'),$('hbl'),$('hbr'), $('contentbase')],{duration:common_duration, transition: common_transition});

    var info_height = $('hbup').getStyle('height').replace('px','');
    var info_height_num = parseInt(info_height);
    var info_top = $('hbup').getStyle('top');
    
    if (info_top == '0px')
    {
        info_trans.start(
        {
            '0': {'top': ['0px','-' + info_height + 'px']},
            '1': {'top': [info_height + 'px','0px']},
            '2': {'top': [info_height + 'px','0px']},
            '3': {'top': [info_height + 'px','0px']},
            '4': {'top': [info_height + 'px','0px']},
            '5': {'top': [(info_height_num + 40).toString() + 'px','40px']}
        });
    }
    else
    {
        info_trans.start(
        {
            '0': {'top': ['-' + info_height + 'px','0px']},
            '1': {'top': ['0px',info_height + 'px']},
            '2': {'top': ['0px',info_height + 'px']},
            '3': {'top': ['0px',info_height + 'px']},
            '4': {'top': ['0px',info_height + 'px']},
            '5': {'top': ['40px',(info_height_num + 40).toString() + 'px']}            
        });    
    }
}

function DisposeCListsIfStale()
{
    $$('ul#CountyList').each(function(clist)
    {
        var age = clist.get('age');
        if (age == 'stale')
        {
            clist.set('listforstate', 'disposing');
            clist.dispose();
        }
    });  
}

function StateSelected()
{
    ProcessSelectedState(chosenoption=this.options[this.selectedIndex].value);
}

function ProcessSelectedState(selection_text)
{
    if (selection_text!='nothing')
    {       
        var show_counties =  $('showcounties');
        var initialized = show_counties.get('initialized');
        
        if (!initialized)
        {
            show_counties.set('initialized', 'true');
            // Set the tween oncomplete
            $('showcounties').set('tween',
            {
                onComplete: function() {DisposeCListsIfStale();}
            });    
        }
        
        $$('ul#CountyList').each(function(clist)
        {
            clist.set('age', 'stale');
        });
        
        var county_list = $('CountyList');
        
        var cur_state = '';
        if (county_list)
        {
            cur_state = county_list.get('listforstate');
        }
        
        if (cur_state != selection_text)
        {                      
            var jsonRequest = new Request.JSON(
            {   url: "/countiesinstate/" + selection_text,
                method: 'get', 
                onSuccess: function(data)
                {       
                    var new_list  = new Element('ul',{id: 'CountyList'});
                    new_list.set('listforstate',selection_text);
                    
                    data.each(function(county, index)
                    {
                        list_item = new Element('li',{'text': county.name + '      (lat: ' + county.primary_latitude + ' long: ' + county.primary_longitude + ')' }).inject(new_list);
                    });
                    
                    var cur_opacity = $('showcounties').get('opacity');
                    var records_returned = data.length;
                                      
                    if (records_returned == 0 && cur_opacity >0)
                    {
                        $('showcounties').set('tween', {
                            duration: 150,
                            transition: 'sine:out'                        
                        });
                            
                        $('showcounties').tween('opacity',0);
                    }
                    else
                    {
                        $('showcounties').set('tween', {
                            duration: 150,
                            transition: 'sine:in'
                        });
                        
                        DisposeCListsIfStale();                        
                                       
                        $('CountyData').appendChild(new_list);
                        
                        var spiffy_county_data = $('CountyList');
                        var step = 0;
                        
                        spiffy_county_data.getElements('li').each(function(li)
                        {
                            var color;
                            if (step++ %2 == 0)
                            {
                                color = '#C8B5A7';                       
                            }
                            else
                            {
                                color = '#8C796B';                       
                            }
        
                            li.setStyles(
                            {
                                
                              'background-color': color,
                              fontWeight: 'bold'
                            });
                        });
                        
                        new Sortables(spiffy_county_data, {clone: true, revert: true, opacity: 0.7});
                        
                        if (records_returned >0 && cur_opacity == 0)
                        {
                            $('showcounties').tween('opacity',1);
                        }
                    }
                    
                }}).send();
        }
    }
}


window.addEvent('domready', function()
{
    $$('.listcombo').each(function(ulist){
            new ListCombo(ulist, ProcessSelectedState, '#8C796B', '#786557');
    });
        
    $('htaglink').addEvent('click', ToggleHeaderInfo);            
});


