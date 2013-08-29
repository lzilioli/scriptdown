module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {
      dist: {
        files: [{
          expand: true,
          cwd: 'www/gui/sass/',
          src: ['*.scss'],
          dest: 'www/gui/build/css',
          ext: '.css'
        }]
      }
    },
    copy: {
      main: {
        files: [{
          expand: true,
          cwd: 'www/gui/scripts/',
          src: ['**/*.js'],
          dest: 'www/gui/build/scripts/'}
          ]
        }
      },
      watch: {
        css: {
          files: 'www/gui/sass/**/*.scss',
          tasks: ['sass'],
          options: {
            livereload: true
          }
        },
        scripts: {
          files: 'www/gui/scripts/**/*.js',
          tasks: ['copy'],
          options: {
            livereload: true
          }
        }
      },
    clean: ['www/gui/build/']
  });

  
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-clean');

  grunt.registerTask('default', ['clean', 'sass', 'copy']);

};
