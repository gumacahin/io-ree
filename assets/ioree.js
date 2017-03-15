/**
 * ioree.js
 *
 * Defines io an object that has the stuff needed by ioree.
 *
 * @package IOREE
 * @author Marco Enrico Alviar
 * @copyright 2012 Author
 */

(function(){ // namespace start
  io = {
    clear: function(){
      $$('#re, #flags, #string').each(function(el){el.value = '';});
      $('output').innerHTML = 'fields cleared';
    },
    loading:function(){
      if (!this.gif) {
        this.gif = new Element('img', {
          src:'assets/ajax-loader.gif',
          alt:'loading...',
          style: 'margin-left:10px;'
        });
        this.gif.inject($$('h1')[0]);
      }
      this.gif.setStyle('display', 'inline');
    },
    clearLoading:function(){
      try {
        this.gif.setStyle('display', 'none');
      }catch(e){}
    },
    init:function(){
      // clearing fields
      $('bn_clear').addEvent('click', function(){
        io.clear();
      });
      this.request = new Request.HTML({
        link: 'cancel',
        url:'/',
        update:$('output'),
        onRequest:function(){
          //set spiniier
        },
        onComplete:function(){
          io.req = undefined;
          // clear spinner
        }
      }),

      // where the magic is
      $$('#re,#flags,#string').each(function(el){
        new Observer(el, function(){
            this.request.post({
              re:$('re').value,
              flags:$('flags').value,
              string:$('string').value
            });
        }.bind(this), {delay:500});
          //}
      }.bind(this));

      // reset the cheat sheet
      $('bn_reset').addEvent('click', function(){
        var def;
        $$('dl').each(function(dl){
          dl.setStyle('z-index', 0);
          if (def = dl.retrieve('def')) {
            dl.setStyles(def);
          }
        });
      });

      // init dragging
      $$('dl').each(function(drag){
        new Drag.Move(drag, {
                handle: drag.getElement('dt'),
                onBeforeStart:function(el){
                  $$('dl').setStyle('z-index',0);
                  el.setStyle('z-index', 1);
                  if (!drag.retrieve('def')) {
                    drag.store('def', {
                      top:drag.getStyle('top'),
                      left:drag.getStyle('left')
                    });
                  }
                },
                onComplete:function(){
                  $$('div.help').destroy();
                }
        });
      });
    }
  }
})(); // namespace end

window.addEvent('domready',function(){
  io.init();
});
