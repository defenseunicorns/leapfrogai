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
  <path d="M16,31.36	C8.082,31.36,1.64,24.918,1.64,17V0.64h28.72V17C30.36,24.918,23.918,31.36,16,31.36z M16.36,23.352v7.284	C23.716,30.444,29.64,24.4,29.64,17V1.36H16.36v13.329c0.576,0.158,1,0.686,1,1.312s-0.425,1.153-1,1.312v5.318	c3.495-0.187,6.28-3.089,6.28-6.63c0-1.774-0.69-3.441-1.944-4.695l0.51-0.509c1.39,1.39,2.155,3.238,2.155,5.204	C23.36,19.938,20.252,23.163,16.36,23.352z M2.36,1.36V17c0,7.4,5.925,13.444,13.28,13.636V17.312c-0.576-0.158-1-0.686-1-1.312	s0.424-1.153,1-1.312V9.37C12.145,9.558,9.36,12.46,9.36,16c0,1.772,0.691,3.44,1.945,4.695l-0.51,0.51	C9.406,19.813,8.64,17.965,8.64,16c0-3.938,3.108-7.163,7-7.351V1.36H2.36z M16,15.36c-0.353,0-0.64,0.287-0.64,0.64	s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S16.353,15.36,16,15.36z"></path>
</svg>