exports.plugins = [
  require("remark-preset-lint-consistent"),
  require("remark-preset-lint-recommended"),
  [require("remark-lint-list-item-indent"), false],
  [require("remark-lint-maximum-line-length"), 1024],
  [require("remark-lint-unordered-list-marker-style"), "consistent"],
  require("remark-lint-heading-whitespace"),
  require("remark-validate-links"),
  require("remark-frontmatter"),
  [
    require("remark-retext"),
    require("unified")().use({
      plugins: [
        require("retext-english"),
        require("retext-syntax-urls"),
        [
          require("retext-sentence-spacing"),
          {
            preferred: 1
          }
        ],
        require("retext-repeated-words"),
        require("retext-usage"),
        require("retext-indefinite-article"),
        require("retext-redundant-acronyms"),
        [
          require("retext-contractions"),
          {
            straight: true,
            allowLiteral: true
          }
        ],
        require("retext-diacritics"),
        [
          require("retext-quotes"),
          {
            preferred: "straight"
          }
        ],
        require("retext-passive")
      ]
    })
  ]
];
