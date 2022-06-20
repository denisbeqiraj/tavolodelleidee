from py3pin.Pinterest import Pinterest

pinterest = Pinterest(email="startupgarage@supsi.ch", password="pinGarageSG177", username="startupgarage0118")
# pinterest.login()


def search(keyword):
    search_batch = pinterest.search(scope='pins', query=keyword)

    # print(search_batch[0]) il primo è un profilo di pinterest inerente alla parola cercata
    # print(search_batch[1]["images"]["736x"]["url"]) stampa l'url dell'immagine
    # print(search_batch[1]["is_promoted"]) True sono le pubblicità, sponsorizzati da ..

    image_url = []
    image_link = []
    image_videos = []  # TODO da valutare se toglierlo

    for pins in search_batch:
        if "images" in pins.keys() and pins["is_promoted"] is False and len(image_url) < 5:
            image_url.append(pins["images"]["736x"]["url"])
            image_link.append(pins["link"])
            if pins["videos"] is not None:
                image_videos.append(pins["videos"]["video_list"]["V_HLSV4"]["url"])

    data = {
        "all_data": {
            "word": keyword,
            "urls": image_url,
            "links": image_link,
            "urls_videos": image_videos
        }
    }

    return data


my_keyword = 'sesso'
data_receive = search(my_keyword)
print(data_receive)

# print(search_batch[1].keys())

# dict_keys(['rich_summary', 'sponsorship', 'domain', 'carousel_data', 'tracking_params', 'is_stale_product',
# 'is_promotable', 'is_oos_product', 'did_its', 'is_quick_promotable', 'type', 'videos', 'debug_info_html',
# 'is_downstream_promotion', 'is_eligible_for_web_closeup', 'reaction_counts', 'is_eligible_for_related_products',
# 'embed', 'story_pin_data', 'is_eligible_for_pdp', 'is_uploaded', 'has_required_attribution_provider', 'title',
# 'images', 'aggregated_pin_data', 'alt_text', 'id', 'is_prefetch_enabled', 'is_promoted', 'created_at', 'grid_title',
# 'image_crop', 'story_pin_data_id', 'pinner', 'description', 'promoter', 'repin_count', 'promoted_is_removable',
# 'access', 'shopping_flags', 'ad_match_reason', 'dominant_color', 'board', 'image_signature', 'attribution', 'link'])
