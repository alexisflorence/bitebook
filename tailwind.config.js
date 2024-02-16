/* Configuration file for tailwind CSS
Tailwind is a utility first CSS framework for rapidly building 
custom user interfaces*/

/* 
1. Apply Tailwind's utility classes to any HTML files within the templates directory.
2. Allow for theme customization through the theme.extend property, though no customizations are specified in the provided code.
3. Use no additional plugins beyond Tailwind's default set.
*/

/** @type {import('tailwindcss').Config} */
module.exports = {
  // where to look for classes in the project
  content: [
    // tailwind will scan all HTML files within the templates directory
    "./templates/**/*.html",
  ],
  // to customize default design
  theme: {
    // extends tailwinds default theme rather than overriding it completely
    // you can add custome values
    extend: {},
  },
  // This array can be used to add additional plugins to Tailwind CSS,
  //extending its functionality
  plugins: [],
};
