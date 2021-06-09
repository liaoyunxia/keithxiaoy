// https://browsersync.io/docs/gulp
// SO: https://stackoverflow.com/a/35590417
// https://dezoito.github.io/2016/01/06/django-automate-browsersync.html

// SO: https://stackoverflow.com/questions/22115400/why-do-we-need-to-install-gulp-globally-and-locally

var gulp = require('gulp')
var browserSync = require('browser-sync').create()

gulp.task('default', function () {
    browserSync.init({
        notify: false,
        proxy: 'localhost:8000'
    })
    gulp.watch(['jk_p2p_app/**/*.{css,js,html,py}'], browserSync.reload)
})
