'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var livereload = require('gulp-livereload');
var concat = require('gulp-concat');
var lr = require('tiny-lr');
var server = lr();


gulp.task('styles', function (done) {
  return gulp.src('css/main.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('dist/css'))
    .pipe(livereload(server));
});

gulp.task('scripts', function (done) {
  return gulp.src(['node_modules/jquery/dist/jquery.min.js', 'js/**/*.js'])
    .pipe(concat('main.js'))
    .pipe(gulp.dest('dist/js/'))
    .pipe(livereload(server))
});

gulp.task('lr-server', function() {
  server.listen(35729, function(err) {
      if(err) return console.log(err);
  });
})

gulp.task('default', function() {
  gulp.start('lr-server', 'styles', 'scripts');
  gulp.watch('css/**/*', function(event) {
    gulp.start('styles');
  })
  gulp.watch('js/**/*', function(event) {
    gulp.start('scripts');
  })
});