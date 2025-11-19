# Prevent generation of pages for collection items with no_page: true
Jekyll::Hooks.register :documents, :post_write do |doc|
  if doc.collection.label == 'members' && doc.data['no_page'] == true
    # Delete the generated file
    FileUtils.rm_f(doc.destination(doc.site.dest))
  end
end
