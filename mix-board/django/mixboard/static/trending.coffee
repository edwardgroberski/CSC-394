$(document).ready ->
  $.get '/song/trending/10/', (response) ->
    $('#trendingContainer').html response

    $('#chooseForkNameForm').submit (e) ->
      e.preventDefault()
      window.blockChooseForkName();

      forkSongName = $('#chooseForkNameForm #forkSongName')
      name = forkSongName.val()

      postData =
        'song': window.forkSong
        'name': name

      $.post '/song/fork/', postData, (response) ->
        if /^\d+$/.test(response)
          window.location.href = "/song/edit/#{response}/"
        else
          if response is 'dup_name'
            $('#chooseForkNameForm #error').html 'This song name is already in use.'
          else
            $('#chooseForkNameForm #error').html response
          window.unblockChooseForkName()
          forkSongName.focus()
          forkSongName.select()

    $('.trendingSong').mouseover (e) ->
      target =
        if $(e.target).is('.trendingSong')
          $(e.target)
        else
          $(e.target).parents('.trendingSong')

      if not $(e.target).is('.forkSongButton')
        target.addClass('buttonNoHover')
      else
        target.addClass('buttonBorder')

    $('.trendingSong').mouseout (e) ->
      target =
        if $(e.target).is('.trendingSong')
          $(e.target)
        else
          $(e.target).parents('.trendingSong')

      target.removeClass('buttonNoHover').removeClass('buttonBorder')

    $('.trendingSong').click (e) ->
      target =
        if $(e.target).is('.trendingSong')
          $(e.target)
        else
          $(e.target).parents('.trendingSong')

      if not $(e.target).is('.forkSongButton')
        songId   = target.attr 'songId'
        username = target.find('.trendingSongUsername').attr 'name'
        songName = target.find('.trendingSongName').attr 'name'
        url = "/song/show/#{songId}/#{username}/#{songName}/"
        window.location.href = url
      else
        song = $(e.target).parents('.trendingSong')
        window.forkSong = song.attr 'songId'
        name = song.find('.trendingSongName').html()

        forkSongName = $('#chooseForkNameModal #forkSongName')
        forkSongName.val("#{name} [fork]")

        $('#chooseForkNameModal').modal()
        forkSongName.focus()
        forkSongName.select()
