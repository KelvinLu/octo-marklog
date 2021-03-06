// Listings
(function() {
    l = {
        page: 0,
        template: _.template($('#listing-template').html()),
        new_elems: [],
        loading: false,
        end: false,
    };

    l_elem = {
        load_more: $('a#load-more'),
        container: $('div#listings'),
        listings_section: $("div#listings-section"),
    }

    load_more = function() {
        l.page++;

        l.loading = true;

        $.get('/listings/' + l.page.toString() + '.json', function(listings) {
            $.each(listings, function(i, listing) {
                elem = l.template(listing);
                l_elem.container.append(elem);
            });
        }, 'json').
            error(function(e){
                if (e.status == 404) {
                    l_elem.load_more.remove();
                    l.end = true;
                }
            }).
            always(function(){
                l.loading = false;
            });
    };

    l_elem.load_more.click(load_more);

    l_elem.listings_section.scroll(function(){
        section = l_elem.listings_section;
        container = l_elem.container;
        if (!l.loading && !l.end && (section.scrollTop() + section.height() > container.height() - 10)) {
            load_more();
        }
    });

    load_more();
})();

// Changing pages
(function() {
    p = {
        template: _.template($('#post-template').html()),
    };

    p_elem = {
        post_section: $('div#post-section'),
        listings_section: $('div#listings-section'),

        hide_post: $('a#hide-post'),
        container: $('div#post-container'),
        post_elem: undefined,
    }


    loadPost = function(post_hash) {
        return $.get('/post/' + post_hash + '.json', function(post) {
            old_post_elem = p_elem.post_elem;
            post_elem = $(p.template(post));
            p_elem.container.prepend(post_elem);

            if (old_post_elem) {
                delay_ms = 500;
                old_post_elem.css({
                    '-webkit-animation': 'fadeOut ' + delay_ms.toString() + 'ms cubic-bezier(.17,.67,.42,.99)',
                    'animation': 'fadeOut ' + delay_ms.toString() + 'ms cubic-bezier(.17,.67,.42,.99)',
                    'opacity': '0',
                    'pointer-events': 'none',
                });
                post_elem.css({
                    '-webkit-animation': 'fadeIn ' + delay_ms.toString() + 'ms cubic-bezier(.17,.67,.42,.99)',
                    'animation': 'fadeIn ' + delay_ms.toString() + 'ms cubic-bezier(.17,.67,.42,.99)',
                    'opacity': '1',
                    'pointer-events': 'auto',
                });
                window.setTimeout(function (e) {
                    e.remove();
                }, delay_ms, old_post_elem);
            }
            p_elem.post_elem = post_elem;

            p_elem.post_section.trigger('post:' + (old_post_elem ? 'change' : 'new'), [post]);
            p_elem.post_section.trigger('post:highlight', [$('pre code', p_elem.post_elem)]);
        }, 'json');
    };

    hidePost = function() {
        p_elem.post_section.css({
            '-webkit-animation': 'fadeOutRight 500ms cubic-bezier(.17,.67,.42,.99)',
            'animation': 'fadeOutRight 500ms cubic-bezier(.17,.67,.42,.99)',
            'opacity': '0',
            'pointer-events': 'none',
        });

        if (post_elem = p_elem.post_elem) { post_elem.css({ 'pointer-events': 'none' }); }

        p_elem.post_section.trigger('post:hide');
    };

    showPost = function(post_hash) {
        loadPost(post_hash).done(function(){
            p_elem.post_section.css({
                '-webkit-animation': 'fadeInRight 500ms cubic-bezier(.17,.67,.42,.99)',
                'animation': 'fadeInRight 500ms cubic-bezier(.17,.67,.42,.99)',
                'opacity': '1',
                'pointer-events': 'auto',
            });
        });
    };

    hashChange = function(event) {
        hash = location.hash.slice(1);

        if (!hash && !!event)
            hidePost();
        else
            showPost(hash);
    };

    if (location.hash && (hash = location.hash.slice(1))) showPost(hash);

    window.addEventListener('hashchange', hashChange, false);
})();

// Headers
(function() {
    h_elems = {
        listings_header: $('div#listings-header'),
        listings: $('div#listings'),
        listings_section: $('div#listings-section'),
        listings_header_template: _.template($('#listings-header-template').html()),

        post_header: $('div#post-header'),
        post: $('div#post'),
        post_section: $('div#post-section'),
        post_header_template: _.template($('#post-header-template').html()),
        post_title: $('span#post-title.title'),

        html_title: $('title#html-title'),
    };

    h = {
        atListingTop: true,
        atPostTop: true,
        slideTime: 100,

        meta: {
            post_title: '',
        },
    };

    minimalListingHeader = function() {
        h_elems.desc.slideUp(h.slideTime);
        h_elems.listings_title.animate({ 'font-size': '1em' }, h.slideTime);
        h_elems.listings_header.animate({ 'padding-top': '0.2em', 'padding-bottom': '0.2em' }, h.slideTime);
    };

    maximalListingHeader = function() {
        h_elems.desc.slideDown(h.slideTime);
        h_elems.listings_title.animate({ 'font-size': '2em' }, h.slideTime);
        h_elems.listings_header.animate({ 'padding-top': '4em', 'padding-bottom': '6em' }, h.slideTime);
    };

    minimalPostHeader = function() {
        h_elems.post_title.animate({ 'font-size': '1em' }, h.slideTime);
        h_elems.post_header.animate({ 'padding': '0.2em' }, h.slideTime);
    };

    maximalPostHeader = function() {
        h_elems.post_title.animate({ 'font-size': '2em' }, h.slideTime);
        h_elems.post_header.animate({ 'padding': '2em' }, h.slideTime);
    };

    init = function() {
        h_elems.listings.css({ 'padding-top': h_elems.listings_header.outerHeight(true) });
        h_elems.listings_header.css({ 'max-width': h_elems.listings.width() });

        h_elems.listings_section.scroll(function(e) {
            if (h_elems.listings_section.scrollTop() > 50) {
                if (h.atListingTop) {
                    minimalListingHeader();
                }
                h.atListingTop = false;
            } else {
                if (!h.atListingTop) {
                    maximalListingHeader();
                }
                h.atListingTop = true;
            }
        });

        h_elems.post_section.scroll(function(e) {
            if (h_elems.post_section.scrollTop() > 50) {
                if (h.atPostTop) {
                    minimalPostHeader();
                }
                h.atPostTop = false;
            } else {
                if (!h.atPostTop) {
                    maximalPostHeader();
                }
                h.atPostTop = true;
            }
        });

        if (!location.hash.slice(1))
            h_elems.post_section.trigger('post:hide');
    };

    change_post_title = function(post_title) {
        h_elems.html_title.html(post_title + ' &mdash; ' + h.meta.blog_title);
        h_elems.post_title.html(post_title);
        h.meta.post_title = post_title;
    };

    exec_js = function() {
        if (c = $('code.marklog-exec').text().trim()) {
            console.log("marklog-exec:\n" + c.split('\n').map(function(l) { return "> " + l; }).join('\n'));
            eval(c);
        }
    }

    $.get('meta.json', function(meta){
        h.meta = _.extend(h.meta, meta);

        listings_header = h_elems.listings_header_template(h.meta);
        h_elems.listings_header.append(listings_header);

        post_header = h_elems.post_header_template(h.meta);
        h_elems.post_header.append(post_header);

        h_elems.listings_title = $("span#listings-title.title");
        h_elems.desc = $("div#blog-desc");

        h_elems.post_title = $('span#post-title.title');
    }, 'json').done(init);

    h_elems.post_section.on('post:new', function(event, post){
        change_post_title(post.post_title);
        exec_js();
    });

    h_elems.post_section.on('post:change', function(event, post){
        change_post_title(post.post_title);
        minimalPostHeader();
        exec_js();
    });

    h_elems.post_section.on('post:hide', function(event){
        h_elems.html_title.html(h.meta.blog_title);
    });
})();

// hljs
(function(){
    h_elem = {
        post: $("div#post"),
        post_section: $("div#post-section"),
    };

    h_elems.post_section.on('post:highlight', function(event, blocks) {
        blocks.each(function(i, block){
            hljs.highlightBlock(block);
        });
    });
})();
