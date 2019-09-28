program Source9

  var
    s: integer;
    i: integer;
    acc: integer

  begin

    read s;
    i := 1;
    acc := 0;
    while i <= s
    begin
        acc := acc + i;
        i := i + 1
    end

  end.
