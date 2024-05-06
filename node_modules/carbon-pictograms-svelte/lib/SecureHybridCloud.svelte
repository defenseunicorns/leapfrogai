<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M19,31.36c-3.507,0-6.36-2.854-6.36-6.36	v-7.223l6.36-3.18l6.36,3.18V25C25.36,28.507,22.507,31.36,19,31.36z M13.36,18.223V25c0,3.11,2.53,5.64,5.64,5.64	s5.64-2.529,5.64-5.64v-6.777L19,15.402L13.36,18.223z M11,19.64l-3.644,0.004C3.994,19.186,1.36,15.94,1.36,12.255	c0-3.933,3.195-7.133,7.122-7.133c0.932,0,1.842,0.18,2.707,0.535c0.175,0.073,0.381-0.006,0.463-0.181	c1.17-2.5,3.705-4.117,6.457-4.117c3.791,0,6.916,2.969,7.113,6.758c0.01,0.182,0.153,0.328,0.335,0.341	c2.851,0.195,5.084,2.59,5.084,5.454c0,2.533-1.647,5.056-3.752,5.746l0.225,0.684c2.382-0.779,4.248-3.604,4.248-6.429	c0-3.135-2.366-5.774-5.443-6.143c-0.367-4.023-3.739-7.13-7.81-7.13c-2.918,0-5.614,1.649-6.959,4.23	c-0.859-0.31-1.755-0.468-2.669-0.468c-4.324,0-7.841,3.523-7.841,7.853c0,4.104,2.845,7.587,6.667,8.105H11V19.64z"></path>
</svg>